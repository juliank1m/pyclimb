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
import socket
import hmac
import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib import error as urllib_error
from urllib import request as urllib_request

from .harness import get_harness_code
from .sandbox import (
    is_sandbox_enabled,
    is_docker_available,
    is_sandbox_required,
    run_in_sandbox,
    run_function_in_sandbox,
    SandboxResult
)
try:
    from django.conf import settings
except Exception:  # pragma: no cover - safety for non-Django contexts
    settings = None


# Safety constants
DEFAULT_TIMEOUT_SECONDS = 2
MAX_OUTPUT_BYTES = 65536  # 64KB max output
MAX_CODE_BYTES = 50000    # 50KB max code
REMOTE_REQUEST_TIMEOUT_BUFFER_SECONDS = 25

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


def _get_remote_judge_url() -> str:
    if settings is not None:
        configured = getattr(settings, 'PYCLIMB_REMOTE_JUDGE_URL', '')
        if configured:
            return configured
    return os.environ.get('PYCLIMB_REMOTE_JUDGE_URL', '')


def _get_remote_judge_token() -> str:
    if settings is not None:
        configured = getattr(settings, 'PYCLIMB_REMOTE_JUDGE_TOKEN', '')
        if configured:
            return configured
    return os.environ.get('PYCLIMB_REMOTE_JUDGE_TOKEN', '')


def _check_remote_sandbox_mode() -> bool:
    """Remote judge mode is considered active only with URL + auth token."""
    return bool(_get_remote_judge_url() and _get_remote_judge_token())


def _sandbox_required() -> bool:
    """
    Require sandboxing for untrusted execution in production-like contexts.
    Defaults to requiring sandbox when DEBUG is false, unless explicitly disabled.
    """
    return is_sandbox_required()


def get_secure_execution_status() -> dict:
    """
    Summarize whether secure execution is currently available.

    A secure backend is either:
    - local Docker sandbox mode, or
    - remote judge mode (authenticated API).
    """
    local_active = _check_sandbox_mode()
    remote_active = _check_remote_sandbox_mode()
    required = _sandbox_required()

    reason = ''
    if required and not (local_active or remote_active):
        if _get_remote_judge_url() and not _get_remote_judge_token():
            reason = (
                'Secure sandboxed execution is required, but '
                'PYCLIMB_REMOTE_JUDGE_TOKEN is missing.'
            )
        else:
            reason = (
                'Secure sandboxed execution is required, but no secure '
                'execution backend is configured.'
            )

    return {
        'required': required,
        'local_active': local_active,
        'remote_active': remote_active,
        'active': local_active or remote_active,
        'reason': reason,
    }


def _sandbox_required_message() -> str:
    status = get_secure_execution_status()
    return status['reason'] or 'Sandboxing is required for code execution.'


def _sign_remote_payload(timestamp: str, body: bytes, token: str) -> str:
    payload = timestamp.encode('utf-8') + b'.' + body
    digest = hmac.new(token.encode('utf-8'), payload, hashlib.sha256).hexdigest()
    return f'sha256={digest}'


def _run_in_remote_sandbox(payload: dict, timeout: int) -> SandboxResult:
    """
    Execute code via remote sandbox API.

    Expected response JSON keys:
    - stdout (str)
    - stderr (str)
    - exit_code (int)
    - timed_out (bool)
    - error (optional str)
    """
    url = _get_remote_judge_url().rstrip('/') + '/execute'
    token = _get_remote_judge_token()

    body = json.dumps(payload).encode('utf-8')
    timestamp = str(int(time.time()))
    signature = _sign_remote_payload(timestamp, body, token)

    req = urllib_request.Request(
        url=url,
        data=body,
        method='POST',
        headers={
            'Content-Type': 'application/json',
            'X-PyClimb-Timestamp': timestamp,
            'X-PyClimb-Signature': signature,
        },
    )

    request_timeout = max(timeout + 3, timeout + REMOTE_REQUEST_TIMEOUT_BUFFER_SECONDS)

    try:
        with urllib_request.urlopen(req, timeout=request_timeout) as response:
            raw = response.read()
    except urllib_error.HTTPError as e:
        error_body = e.read().decode('utf-8', errors='replace')[:500]
        return SandboxResult(
            stdout='',
            stderr='',
            exit_code=-1,
            timed_out=False,
            error=f'Remote judge HTTP {e.code}: {error_body}',
        )
    except urllib_error.URLError as e:
        return SandboxResult(
            stdout='',
            stderr='',
            exit_code=-1,
            timed_out=False,
            error=f'Remote judge unavailable: {str(e.reason)}',
        )
    except socket.timeout:
        return SandboxResult(
            stdout='',
            stderr='',
            exit_code=-1,
            timed_out=False,
            error='Remote judge request timed out before receiving a response.',
        )
    except Exception as e:
        return SandboxResult(
            stdout='',
            stderr='',
            exit_code=-1,
            timed_out=False,
            error=f'Remote judge request failed: {str(e)}',
        )

    try:
        data = json.loads(raw.decode('utf-8'))
    except Exception:
        return SandboxResult(
            stdout='',
            stderr='',
            exit_code=-1,
            timed_out=False,
            error='Remote judge returned invalid JSON.',
        )

    return SandboxResult(
        stdout=str(data.get('stdout', ''))[:MAX_OUTPUT_BYTES],
        stderr=str(data.get('stderr', ''))[:MAX_OUTPUT_BYTES],
        exit_code=int(data.get('exit_code', -1)),
        timed_out=bool(data.get('timed_out', False)),
        error=data.get('error'),
    )


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
    if _check_remote_sandbox_mode():
        start_time = time.perf_counter()
        sandbox_result = _run_in_remote_sandbox(
            payload={
                'mode': 'stdin',
                'language': 'python',
                'code': code,
                'stdin_input': stdin_input,
                'timeout': int(timeout),
            },
            timeout=int(timeout),
        )
        elapsed_ms = int((time.perf_counter() - start_time) * 1000)
        return RunResult(
            stdout=sandbox_result.stdout,
            stderr=sandbox_result.stderr,
            exit_code=sandbox_result.exit_code,
            timed_out=sandbox_result.timed_out,
            elapsed_ms=elapsed_ms,
            error=sandbox_result.error,
        )
    if _sandbox_required():
        return RunResult(
            stdout='',
            stderr=_sandbox_required_message(),
            exit_code=-1,
            timed_out=False,
            elapsed_ms=0,
            error='Sandbox required'
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
    try:
        harness_code = get_harness_code(entrypoint_type, entrypoint_name)
    except ValueError as e:
        return FunctionCallResult(
            success=False,
            result=None,
            error_type='internal',
            error_message=str(e),
            traceback='',
            timed_out=False,
            elapsed_ms=0
        )
    
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

    if _check_remote_sandbox_mode():
        start_time = time.perf_counter()
        sandbox_result = _run_in_remote_sandbox(
            payload={
                'mode': 'function',
                'language': 'python',
                'code': code,
                'harness_code': harness_code,
                'args_json': args_json,
                'timeout': int(timeout),
            },
            timeout=int(timeout),
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
        return FunctionCallResult(
            success=False,
            result=None,
            error_type=output.get('error', 'unknown'),
            error_message=output.get('message', 'Unknown error'),
            traceback=output.get('traceback', ''),
            timed_out=False,
            elapsed_ms=elapsed_ms
        )

    if _sandbox_required():
        return FunctionCallResult(
            success=False,
            result=None,
            error_type='internal',
            error_message=_sandbox_required_message(),
            traceback='',
            timed_out=False,
            elapsed_ms=0
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
