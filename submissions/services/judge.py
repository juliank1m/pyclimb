"""
Judge service for evaluating submissions against test cases.

This is the main entry point for judging a submission.
It orchestrates:
1. Syntax checking (compile check)
2. Running against each test case
3. Comparing outputs
4. Determining final verdict

Supports two modes:
- STDIN_STDOUT: Traditional stdin/stdout comparison
- FUNCTION_CALL: LeetCode-style function return value comparison
"""

import ast
import json
from dataclasses import dataclass
from typing import Any

from submissions.models import Submission, Verdict, SubmissionStatus
from problems.models import JudgeMode
from .runner import run_python_code, run_function_call, RunResult, FunctionCallResult
from .normalize import outputs_match


@dataclass
class TestCaseResult:
    """Result of running one test case."""
    test_case_id: int
    is_sample: bool
    passed: bool
    verdict: str
    stdout: str
    stderr: str
    expected: str  # Only populated for samples
    input_display: str  # Only populated for samples
    elapsed_ms: int = 0  # Execution time for this test case


@dataclass 
class JudgeResult:
    """Overall result of judging a submission."""
    verdict: str
    test_results: list[TestCaseResult]
    stdout: str  # Combined/summary stdout for display
    stderr: str  # Combined/summary stderr for display
    failed_test_index: int | None  # 1-indexed, for display
    total_time_ms: int = 0  # Total execution time across all test cases


def check_syntax(code: str) -> tuple[bool, str]:
    """
    Check if Python code has valid syntax.
    
    Returns (is_valid, error_message).
    """
    try:
        ast.parse(code)
        return True, ''
    except SyntaxError as e:
        error_msg = f"Line {e.lineno}: {e.msg}"
        if e.text:
            error_msg += f"\n  {e.text.strip()}"
        return False, error_msg


def values_equal(actual: Any, expected: Any) -> bool:
    """
    Compare two Python values for equality.
    
    For MVP, uses simple deep equality.
    Future: could add tolerance for floats, order-independent list comparison, etc.
    """
    return actual == expected


def format_value_for_display(value: Any) -> str:
    """Format a Python value as a readable string for display."""
    try:
        return json.dumps(value, indent=2)
    except (TypeError, ValueError):
        return repr(value)


def judge_stdin_stdout(submission: Submission) -> JudgeResult:
    """Judge a submission using stdin/stdout mode."""
    code = submission.code
    problem = submission.problem
    
    # Syntax check
    syntax_ok, syntax_error = check_syntax(code)
    if not syntax_ok:
        return JudgeResult(
            verdict=Verdict.COMPILE_ERROR,
            test_results=[],
            stdout='',
            stderr=f"Syntax Error:\n{syntax_error}",
            failed_test_index=None,
            total_time_ms=0
        )
    
    test_cases = list(problem.test_cases.order_by('-is_sample', 'id'))
    
    if not test_cases:
        return JudgeResult(
            verdict=Verdict.ACCEPTED,
            test_results=[],
            stdout='No test cases defined.',
            stderr='',
            failed_test_index=None,
            total_time_ms=0
        )
    
    test_results: list[TestCaseResult] = []
    final_verdict = Verdict.ACCEPTED
    failed_index = None
    combined_stdout = ''
    combined_stderr = ''
    total_time_ms = 0
    
    for i, tc in enumerate(test_cases, start=1):
        result = run_python_code(code, tc.input_data)
        total_time_ms += result.elapsed_ms
        
        if result.error:
            tc_verdict = Verdict.RUNTIME_ERROR
            passed = False
        elif result.timed_out:
            tc_verdict = Verdict.TIME_LIMIT
            passed = False
        elif result.exit_code != 0:
            tc_verdict = Verdict.RUNTIME_ERROR
            passed = False
        elif outputs_match(result.stdout, tc.expected_output):
            tc_verdict = Verdict.ACCEPTED
            passed = True
        else:
            tc_verdict = Verdict.WRONG_ANSWER
            passed = False
        
        tc_result = TestCaseResult(
            test_case_id=tc.id,
            is_sample=tc.is_sample,
            passed=passed,
            verdict=tc_verdict,
            stdout=result.stdout if tc.is_sample else '',
            stderr=result.stderr if tc.is_sample else '',
            expected=tc.expected_output if tc.is_sample else '',
            input_display=tc.display_input if tc.is_sample else '',
            elapsed_ms=result.elapsed_ms,
        )
        test_results.append(tc_result)
        
        if not passed and final_verdict == Verdict.ACCEPTED:
            final_verdict = tc_verdict
            failed_index = i
            combined_stdout = result.stdout
            combined_stderr = result.stderr
            if not tc.is_sample:
                break
    
    if final_verdict == Verdict.ACCEPTED:
        combined_stdout = 'All test cases passed!'
    
    return JudgeResult(
        verdict=final_verdict,
        test_results=test_results,
        stdout=combined_stdout,
        stderr=combined_stderr,
        failed_test_index=failed_index,
        total_time_ms=total_time_ms
    )


def judge_function_call(submission: Submission) -> JudgeResult:
    """Judge a submission using function-call (LeetCode) mode."""
    code = submission.code
    problem = submission.problem
    
    # Get entrypoint configuration
    entrypoint_type = problem.entrypoint_type
    entrypoint_name = problem.entrypoint_name
    
    if not entrypoint_name:
        return JudgeResult(
            verdict=Verdict.RUNTIME_ERROR,
            test_results=[],
            stdout='',
            stderr='Problem configuration error: no entrypoint name specified.',
            failed_test_index=None,
            total_time_ms=0
        )
    
    test_cases = list(problem.test_cases.order_by('-is_sample', 'id'))
    
    if not test_cases:
        return JudgeResult(
            verdict=Verdict.ACCEPTED,
            test_results=[],
            stdout='No test cases defined.',
            stderr='',
            failed_test_index=None,
            total_time_ms=0
        )
    
    test_results: list[TestCaseResult] = []
    final_verdict = Verdict.ACCEPTED
    failed_index = None
    combined_stdout = ''
    combined_stderr = ''
    total_time_ms = 0
    
    for i, tc in enumerate(test_cases, start=1):
        # Run the function call
        result = run_function_call(
            code=code,
            entrypoint_type=entrypoint_type,
            entrypoint_name=entrypoint_name,
            args_json=tc.input_data
        )
        total_time_ms += result.elapsed_ms
        
        # Parse expected output
        try:
            expected_value = json.loads(tc.expected_output)
        except json.JSONDecodeError:
            # This shouldn't happen if validation is working
            tc_verdict = Verdict.RUNTIME_ERROR
            passed = False
            actual_display = ''
            error_msg = f'Invalid expected output JSON: {tc.expected_output}'
            result = FunctionCallResult(
                success=False, result=None, error_type='internal',
                error_message=error_msg, traceback='', timed_out=False,
                elapsed_ms=result.elapsed_ms
            )
        
        if result.success:
            # Compare return values
            if values_equal(result.result, expected_value):
                tc_verdict = Verdict.ACCEPTED
                passed = True
            else:
                tc_verdict = Verdict.WRONG_ANSWER
                passed = False
            actual_display = format_value_for_display(result.result)
            error_display = ''
        else:
            # Execution failed
            passed = False
            actual_display = ''
            
            if result.timed_out:
                tc_verdict = Verdict.TIME_LIMIT
                error_display = 'Time limit exceeded'
            elif result.error_type == 'syntax':
                tc_verdict = Verdict.COMPILE_ERROR
                error_display = f"Syntax Error: {result.error_message}"
            elif result.error_type in ('import', 'runtime'):
                tc_verdict = Verdict.RUNTIME_ERROR
                error_display = result.traceback or result.error_message
            else:
                tc_verdict = Verdict.RUNTIME_ERROR
                error_display = result.error_message
        
        tc_result = TestCaseResult(
            test_case_id=tc.id,
            is_sample=tc.is_sample,
            passed=passed,
            verdict=tc_verdict,
            stdout=actual_display if tc.is_sample else '',
            stderr=error_display if tc.is_sample else '',
            expected=format_value_for_display(expected_value) if tc.is_sample else '',
            input_display=tc.display_input if tc.is_sample else '',
            elapsed_ms=result.elapsed_ms,
        )
        test_results.append(tc_result)
        
        if not passed and final_verdict == Verdict.ACCEPTED:
            final_verdict = tc_verdict
            failed_index = i
            combined_stdout = actual_display
            combined_stderr = error_display if 'error_display' in dir() else ''
            if not tc.is_sample:
                break
    
    if final_verdict == Verdict.ACCEPTED:
        combined_stdout = 'All test cases passed!'
    
    return JudgeResult(
        verdict=final_verdict,
        test_results=test_results,
        stdout=combined_stdout,
        stderr=combined_stderr,
        failed_test_index=failed_index,
        total_time_ms=total_time_ms
    )


def judge_submission(submission: Submission) -> JudgeResult:
    """
    Judge a submission against all test cases.
    
    Routes to the appropriate judge based on the problem's judge_mode.
    
    Args:
        submission: The Submission instance to judge
        
    Returns:
        JudgeResult with verdict and per-test-case results
    """
    problem = submission.problem
    
    if problem.judge_mode == JudgeMode.FUNCTION_CALL:
        return judge_function_call(submission)
    else:
        return judge_stdin_stdout(submission)


def run_judge(submission: Submission) -> None:
    """
    Run the judge and update the submission in-place.
    
    This is the function called from the view after submission creation.
    It updates the submission's status, verdict, stdout, stderr, test_results, and execution_time_ms.
    """
    # Mark as running
    submission.status = SubmissionStatus.RUNNING
    submission.save(update_fields=['status'])
    
    try:
        result = judge_submission(submission)
        
        # Convert test results to JSON-serializable format
        test_results_json = [
            {
                'test_id': tr.test_case_id,
                'is_sample': tr.is_sample,
                'passed': tr.passed,
                'verdict': tr.verdict,
                'stdout': tr.stdout,
                'stderr': tr.stderr,
                'expected': tr.expected,
                'input_display': tr.input_display,
                'elapsed_ms': tr.elapsed_ms,
            }
            for tr in result.test_results
        ]
        
        # Update submission with results
        submission.verdict = result.verdict
        submission.stdout = result.stdout
        submission.stderr = result.stderr
        submission.test_results = test_results_json
        submission.execution_time_ms = result.total_time_ms
        submission.status = SubmissionStatus.DONE
        submission.save(update_fields=['verdict', 'stdout', 'stderr', 'test_results', 'execution_time_ms', 'status'])
        
    except Exception as e:
        # Internal error - not the user's fault
        submission.verdict = Verdict.RUNTIME_ERROR
        submission.stderr = f"Internal judge error: {str(e)}"
        submission.status = SubmissionStatus.DONE
        submission.save(update_fields=['verdict', 'stderr', 'status'])
