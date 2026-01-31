"""
Code execution runner with safety constraints.

Executes user code in a subprocess with:
- Time limit enforcement
- Output size limits
- Isolated temporary directory
- No network access (best-effort via short timeout)

When sandbox mode is enabled (PYCLIMB_USE_SANDBOX=true), code runs in
isolated Docker containers with full network/filesystem isolation.

WARNING: Without sandbox mode, this is MVP-level safety. Not suitable for
untrusted public internet use. See SECURITY.md for production requirements.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .harness import get_harness_code
from .sandbox import (
    is_sandbox_enabled,
    is_docker_available,
    run_in_sandbox,
    run_function_in_sandbox,
    SandboxResult
)


# Safety constants
DEFAULT_TIMEOUT_SECONDS = 2
MAX_OUTPUT_BYTES = 65536  # 64KB max output
MAX_CODE_BYTES = 50000    # 50KB max code

# Cache Docker availability check
_docker_available = None


def _get_python_bin() -> str:
    env_bin = os.environ.get('PYCLIMB_PYTHON_BIN')
    if env_bin:
        return env_bin
    if sys.executable:
        return sys.executable
    for candidate in ('python3', 'python'):
        found = shutil.which(candidate)
        if found:
            return found
    return 'python3'


def _check_sandbox_mode() -> bool:
    """Check if sandbox mode should be used."""
    global _docker_available
    
    if not is_sandbox_enabled():
        return False
    
    if _docker_available is None:
        _docker_available = is_docker_available()
    
    return _docker_available


@dataclass
class RunResult:
    """Result of executing user code (for stdin/stdout mode)."""
    stdout: str
    stderr: str
    exit_code: int
    timed_out: bool
    elapsed_ms: int = 0  # Wall-clock execution time in milliseconds
    error: str | None = None  # Internal error (not user's fault)


@dataclass
class FunctionCallResult:
    """Result of executing user code in function-call mode."""
    success: bool
    result: Any  # The returned value (if success)
    error_type: str | None  # 'syntax', 'import', 'runtime', 'timeout', 'internal'
    error_message: str
    traceback: str
    timed_out: bool
    elapsed_ms: int = 0  # Wall-clock execution time in milliseconds


def run_python_code(code: str, stdin_input: str, timeout: float = DEFAULT_TIMEOUT_SECONDS) -> RunResult:
    """
    Execute Python code in a subprocess (or Docker sandbox if enabled).
    
    Args:
        code: The Python source code to execute
        stdin_input: Data to pass to the program's stdin
        timeout: Maximum execution time in seconds
    
    Returns:
        RunResult with stdout, stderr, exit code, and timeout flag
    """
    if len(code.encode('utf-8')) > MAX_CODE_BYTES:
        return RunResult(
            stdout='',
            stderr='',
            exit_code=-1,
            timed_out=False,
            elapsed_ms=0,
            error='Code exceeds maximum size limit'
        )
    
    # Use Docker sandbox if enabled and available
    if _check_sandbox_mode():
        start_time = time.perf_counter()
        sandbox_result = run_in_sandbox(code, stdin_input, timeout=int(timeout))
        elapsed_ms = int((time.perf_counter() - start_time) * 1000)
        return RunResult(
            stdout=sandbox_result.stdout,
            stderr=sandbox_result.stderr,
            exit_code=sandbox_result.exit_code,
            timed_out=sandbox_result.timed_out,
            elapsed_ms=elapsed_ms,
            error=sandbox_result.error
        )

    # Create a temporary directory for isolation
    with tempfile.TemporaryDirectory(prefix='pyclimb_') as tmpdir:
        # Write code to a temp file
        code_path = Path(tmpdir) / 'solution.py'
        code_path.write_text(code, encoding='utf-8')
        
        try:
            # Run Python in subprocess
            # Using -I flag for isolated mode (ignores PYTHON* env vars, no user site-packages)
            # Using -S flag to skip site.py (faster startup, fewer imports)
            start_time = time.perf_counter()
            result = subprocess.run(
                [_get_python_bin(), '-I', str(code_path)],
                input=stdin_input,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=tmpdir,
                env={
                    # Minimal environment
                    'PATH': '/usr/bin:/bin',
                    'HOME': tmpdir,
                    'TMPDIR': tmpdir,
                    # Prevent Python from writing bytecode
                    'PYTHONDONTWRITEBYTECODE': '1',
                }
            )
            elapsed_ms = int((time.perf_counter() - start_time) * 1000)
            
            # Truncate output if too large
            stdout = result.stdout[:MAX_OUTPUT_BYTES]
            stderr = result.stderr[:MAX_OUTPUT_BYTES]
            
            if len(result.stdout) > MAX_OUTPUT_BYTES:
                stdout += '\n[OUTPUT TRUNCATED]'
            if len(result.stderr) > MAX_OUTPUT_BYTES:
                stderr += '\n[OUTPUT TRUNCATED]'
            
            return RunResult(
                stdout=stdout,
                stderr=stderr,
                exit_code=result.returncode,
                timed_out=False,
                elapsed_ms=elapsed_ms
            )
            
        except subprocess.TimeoutExpired as e:
            elapsed_ms = int((time.perf_counter() - start_time) * 1000)
            return RunResult(
                stdout='',
                stderr='',
                exit_code=-1,
                timed_out=True,
                elapsed_ms=elapsed_ms
            )
        except Exception as e:
            return RunResult(
                stdout='',
                stderr='',
                exit_code=-1,
                timed_out=False,
                elapsed_ms=0,
                error=f'Execution failed: {str(e)}'
            )


def run_function_call(
    code: str,
    entrypoint_type: str,
    entrypoint_name: str,
    args_json: str,
    timeout: float = DEFAULT_TIMEOUT_SECONDS
) -> FunctionCallResult:
    """
    Execute user code in function-call mode.
    
    Writes the user's code as submission.py, creates a harness runner.py,
    passes arguments via input.json, and captures the JSON result.
    
    When sandbox mode is enabled, runs in a Docker container.
    
    Args:
        code: The user's Python source code
        entrypoint_type: 'class' for Solution class, 'function' for bare function
        entrypoint_name: The method/function name to call
        args_json: JSON string of arguments to pass
        timeout: Maximum execution time in seconds
        
    Returns:
        FunctionCallResult with the returned value or error details
    """
    if len(code.encode('utf-8')) > MAX_CODE_BYTES:
        return FunctionCallResult(
            success=False,
            result=None,
            error_type='internal',
            error_message='Code exceeds maximum size limit',
            traceback='',
            timed_out=False,
            elapsed_ms=0
        )
    
    # Get harness code
    harness_code = get_harness_code(entrypoint_type, entrypoint_name)
    
    # Use Docker sandbox if enabled and available
    if _check_sandbox_mode():
        start_time = time.perf_counter()
        sandbox_result = run_function_in_sandbox(
            code, harness_code, args_json, timeout=int(timeout)
        )
        elapsed_ms = int((time.perf_counter() - start_time) * 1000)
        
        if sandbox_result.timed_out:
            return FunctionCallResult(
                success=False,
                result=None,
                error_type='timeout',
                error_message='Time limit exceeded',
                traceback='',
                timed_out=True,
                elapsed_ms=elapsed_ms
            )
        
        if sandbox_result.error:
            return FunctionCallResult(
                success=False,
                result=None,
                error_type='internal',
                error_message=sandbox_result.error,
                traceback='',
                timed_out=False,
                elapsed_ms=elapsed_ms
            )
        
        # Parse JSON output from harness
        stdout = sandbox_result.stdout.strip()
        if not stdout:
            return FunctionCallResult(
                success=False,
                result=None,
                error_type='internal',
                error_message='Harness produced no output',
                traceback=sandbox_result.stderr[:MAX_OUTPUT_BYTES],
                timed_out=False,
                elapsed_ms=elapsed_ms
            )
        
        try:
            output = json.loads(stdout)
        except json.JSONDecodeError:
            return FunctionCallResult(
                success=False,
                result=None,
                error_type='internal',
                error_message=f'Harness output not valid JSON: {stdout[:200]}',
                traceback=sandbox_result.stderr[:MAX_OUTPUT_BYTES],
                timed_out=False,
                elapsed_ms=elapsed_ms
            )
        
        if output.get('ok'):
            return FunctionCallResult(
                success=True,
                result=output['result'],
                error_type=None,
                error_message='',
                traceback='',
                timed_out=False,
                elapsed_ms=elapsed_ms
            )
        else:
            return FunctionCallResult(
                success=False,
                result=None,
                error_type=output.get('error', 'unknown'),
                error_message=output.get('message', 'Unknown error'),
                traceback=output.get('traceback', ''),
                timed_out=False,
                elapsed_ms=elapsed_ms
            )

    # Fallback: run in subprocess (not sandboxed)
    with tempfile.TemporaryDirectory(prefix='pyclimb_fc_') as tmpdir:
        tmppath = Path(tmpdir)
        
        # Write user code as submission.py
        (tmppath / 'submission.py').write_text(code, encoding='utf-8')
        
        # Write harness runner (harness_code already defined above)
        (tmppath / 'runner.py').write_text(harness_code, encoding='utf-8')
        
        # Write input arguments
        (tmppath / 'input.json').write_text(args_json, encoding='utf-8')
        
        try:
            start_time = time.perf_counter()
            result = subprocess.run(
                [_get_python_bin(), 'runner.py'],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=tmpdir,
                env={
                    'PATH': '/usr/bin:/bin',
                    'HOME': tmpdir,
                    'TMPDIR': tmpdir,
                    'PYTHONDONTWRITEBYTECODE': '1',
                    # Add the temp directory to Python path for imports
                    'PYTHONPATH': tmpdir,
                }
            )
            elapsed_ms = int((time.perf_counter() - start_time) * 1000)
            
            # Parse the JSON output from the harness
            stdout = result.stdout.strip()
            if not stdout:
                # No output - harness crashed unexpectedly
                return FunctionCallResult(
                    success=False,
                    result=None,
                    error_type='internal',
                    error_message='Harness produced no output',
                    traceback=result.stderr[:MAX_OUTPUT_BYTES],
                    timed_out=False,
                    elapsed_ms=elapsed_ms
                )
            
            try:
                output = json.loads(stdout)
            except json.JSONDecodeError:
                return FunctionCallResult(
                    success=False,
                    result=None,
                    error_type='internal',
                    error_message=f'Harness output not valid JSON: {stdout[:200]}',
                    traceback=result.stderr[:MAX_OUTPUT_BYTES],
                    timed_out=False,
                    elapsed_ms=elapsed_ms
                )
            
            if output.get('ok'):
                return FunctionCallResult(
                    success=True,
                    result=output['result'],
                    error_type=None,
                    error_message='',
                    traceback='',
                    timed_out=False,
                    elapsed_ms=elapsed_ms
                )
            else:
                return FunctionCallResult(
                    success=False,
                    result=None,
                    error_type=output.get('error', 'unknown'),
                    error_message=output.get('message', 'Unknown error'),
                    traceback=output.get('traceback', ''),
                    timed_out=False,
                    elapsed_ms=elapsed_ms
                )
                
        except subprocess.TimeoutExpired:
            elapsed_ms = int((time.perf_counter() - start_time) * 1000)
            return FunctionCallResult(
                success=False,
                result=None,
                error_type='timeout',
                error_message='Time limit exceeded',
                traceback='',
                timed_out=True,
                elapsed_ms=elapsed_ms
            )
        except Exception as e:
            return FunctionCallResult(
                success=False,
                result=None,
                error_type='internal',
                error_message=f'Execution failed: {str(e)}',
                traceback='',
                timed_out=False,
                elapsed_ms=0
            )
