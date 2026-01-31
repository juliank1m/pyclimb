"""
Docker-based sandbox execution for untrusted code.

Provides secure code execution using disposable Docker containers with:
- No network access
- Memory limits
- CPU limits
- Read-only filesystem
- Dropped capabilities
- Non-root user

Usage:
    result = run_in_sandbox(code, stdin_input, timeout=5)
"""

import json
import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from django.conf import settings


# Default sandbox configuration
DEFAULT_IMAGE = 'pyclimb-sandbox'
DEFAULT_TIMEOUT = 5
DEFAULT_MEMORY = '128m'
DEFAULT_CPUS = '0.5'
MAX_OUTPUT_BYTES = 65536  # 64KB


@dataclass
class SandboxResult:
    """Result of executing code in the sandbox."""
    stdout: str
    stderr: str
    exit_code: int
    timed_out: bool
    error: Optional[str] = None


def is_docker_available() -> bool:
    """Check if Docker is available and running."""
    try:
        result = subprocess.run(
            ['docker', 'info'],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


def is_sandbox_enabled() -> bool:
    """Check if sandbox mode is enabled via settings."""
    return getattr(settings, 'PYCLIMB_USE_SANDBOX', False) or \
           os.environ.get('PYCLIMB_USE_SANDBOX', '').lower() in ('true', '1', 'yes')


def get_sandbox_config() -> dict:
    """Get sandbox configuration from settings or environment."""
    return {
        'image': getattr(settings, 'PYCLIMB_SANDBOX_IMAGE', None) or \
                 os.environ.get('PYCLIMB_SANDBOX_IMAGE', DEFAULT_IMAGE),
        'timeout': int(getattr(settings, 'PYCLIMB_SANDBOX_TIMEOUT', None) or \
                      os.environ.get('PYCLIMB_SANDBOX_TIMEOUT', DEFAULT_TIMEOUT)),
        'memory': getattr(settings, 'PYCLIMB_SANDBOX_MEMORY', None) or \
                  os.environ.get('PYCLIMB_SANDBOX_MEMORY', DEFAULT_MEMORY),
        'cpus': getattr(settings, 'PYCLIMB_SANDBOX_CPUS', None) or \
                os.environ.get('PYCLIMB_SANDBOX_CPUS', DEFAULT_CPUS),
    }


def run_in_sandbox(
    code: str,
    stdin_input: str = '',
    timeout: Optional[int] = None
) -> SandboxResult:
    """
    Execute Python code in a sandboxed Docker container.
    
    Args:
        code: The Python source code to execute
        stdin_input: Data to pass to the program's stdin
        timeout: Maximum execution time in seconds (overrides default)
    
    Returns:
        SandboxResult with stdout, stderr, exit code, and timeout flag
    """
    config = get_sandbox_config()
    if timeout is None:
        timeout = config['timeout']
    
    # Create temporary directory for code
    with tempfile.TemporaryDirectory(prefix='pyclimb_sandbox_') as tmpdir:
        tmppath = Path(tmpdir)
        
        # Write user code
        code_path = tmppath / 'code.py'
        code_path.write_text(code, encoding='utf-8')
        
        # Write stdin input
        input_path = tmppath / 'input.txt'
        input_path.write_text(stdin_input, encoding='utf-8')
        
        # Build Docker command
        docker_cmd = [
            'docker', 'run',
            '--rm',                              # Remove container after execution
            '--network', 'none',                 # No network access
            '--memory', config['memory'],        # Memory limit
            '--cpus', config['cpus'],            # CPU limit
            '--read-only',                       # Read-only root filesystem
            '--tmpfs', '/tmp:size=10m,mode=1777',  # Writable /tmp with size limit
            '--security-opt', 'no-new-privileges',  # Prevent privilege escalation
            '--cap-drop', 'ALL',                 # Drop all capabilities
            '--pids-limit', '50',                # Limit number of processes
            '-v', f'{code_path}:/sandbox/code.py:ro',      # Mount code read-only
            '-v', f'{input_path}:/sandbox/input.txt:ro',   # Mount input read-only
            config['image'],
            'sh', '-c', f'timeout {timeout} python3 /sandbox/code.py < /sandbox/input.txt'
        ]
        
        try:
            # Run Docker container with an outer timeout (slightly longer than inner)
            result = subprocess.run(
                docker_cmd,
                capture_output=True,
                text=True,
                timeout=timeout + 5  # Extra time for container overhead
            )
            
            # Check if inner timeout triggered (exit code 124)
            timed_out = result.returncode == 124
            
            # Truncate output if too large
            stdout = result.stdout[:MAX_OUTPUT_BYTES]
            stderr = result.stderr[:MAX_OUTPUT_BYTES]
            
            if len(result.stdout) > MAX_OUTPUT_BYTES:
                stdout += '\n[OUTPUT TRUNCATED]'
            if len(result.stderr) > MAX_OUTPUT_BYTES:
                stderr += '\n[OUTPUT TRUNCATED]'
            
            return SandboxResult(
                stdout=stdout,
                stderr=stderr,
                exit_code=result.returncode,
                timed_out=timed_out
            )
            
        except subprocess.TimeoutExpired:
            return SandboxResult(
                stdout='',
                stderr='',
                exit_code=-1,
                timed_out=True
            )
        except Exception as e:
            return SandboxResult(
                stdout='',
                stderr='',
                exit_code=-1,
                timed_out=False,
                error=f'Sandbox execution failed: {str(e)}'
            )


def run_function_in_sandbox(
    code: str,
    harness_code: str,
    args_json: str,
    timeout: Optional[int] = None
) -> SandboxResult:
    """
    Execute function-call mode code in a sandboxed Docker container.
    
    Args:
        code: The user's Python source code (submission.py)
        harness_code: The test harness code (runner.py)
        args_json: JSON string of function arguments
        timeout: Maximum execution time in seconds
    
    Returns:
        SandboxResult with JSON output from the harness
    """
    config = get_sandbox_config()
    if timeout is None:
        timeout = config['timeout']
    
    with tempfile.TemporaryDirectory(prefix='pyclimb_sandbox_fc_') as tmpdir:
        tmppath = Path(tmpdir)
        
        # Write files
        (tmppath / 'submission.py').write_text(code, encoding='utf-8')
        (tmppath / 'runner.py').write_text(harness_code, encoding='utf-8')
        (tmppath / 'input.json').write_text(args_json, encoding='utf-8')
        
        # Build Docker command
        docker_cmd = [
            'docker', 'run',
            '--rm',
            '--network', 'none',
            '--memory', config['memory'],
            '--cpus', config['cpus'],
            '--read-only',
            '--tmpfs', '/tmp:size=10m,mode=1777',
            '--security-opt', 'no-new-privileges',
            '--cap-drop', 'ALL',
            '--pids-limit', '50',
            '-v', f'{tmppath}:/sandbox:ro',
            '-w', '/sandbox',
            '-e', 'PYTHONPATH=/sandbox',
            config['image'],
            'sh', '-c', f'timeout {timeout} python3 /sandbox/runner.py'
        ]
        
        try:
            result = subprocess.run(
                docker_cmd,
                capture_output=True,
                text=True,
                timeout=timeout + 5
            )
            
            timed_out = result.returncode == 124
            
            stdout = result.stdout[:MAX_OUTPUT_BYTES]
            stderr = result.stderr[:MAX_OUTPUT_BYTES]
            
            return SandboxResult(
                stdout=stdout,
                stderr=stderr,
                exit_code=result.returncode,
                timed_out=timed_out
            )
            
        except subprocess.TimeoutExpired:
            return SandboxResult(
                stdout='',
                stderr='',
                exit_code=-1,
                timed_out=True
            )
        except Exception as e:
            return SandboxResult(
                stdout='',
                stderr='',
                exit_code=-1,
                timed_out=False,
                error=f'Sandbox execution failed: {str(e)}'
            )
