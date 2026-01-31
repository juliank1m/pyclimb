"""
Tests for the submissions app.

Focuses on:
- Judge logic (verdict assignment)
- Output normalization
- Runner safety constraints
"""
import pytest
from django.test import TestCase
from django.contrib.auth.models import User

from problems.models import Problem, TestCase as ProblemTestCase, JudgeMode
from submissions.models import Submission, Verdict, SubmissionStatus
from submissions.services.normalize import normalize_output, outputs_match
from submissions.services.judge import check_syntax, judge_submission, judge_stdin_stdout
from submissions.services.runner import run_python_code, RunResult


class NormalizeOutputTests(TestCase):
    """Tests for output normalization."""

    def test_normalize_strips_trailing_whitespace(self):
        """Trailing whitespace on lines should be stripped."""
        output = "hello   \nworld  \n"
        expected = "hello\nworld"
        self.assertEqual(normalize_output(output), expected)

    def test_normalize_strips_trailing_newlines(self):
        """Trailing blank lines should be stripped."""
        output = "hello\nworld\n\n\n"
        expected = "hello\nworld"
        self.assertEqual(normalize_output(output), expected)

    def test_normalize_converts_crlf_to_lf(self):
        """Windows line endings should be normalized to Unix."""
        output = "hello\r\nworld\r\n"
        expected = "hello\nworld"
        self.assertEqual(normalize_output(output), expected)

    def test_outputs_match_exact(self):
        """Exact outputs should match."""
        self.assertTrue(outputs_match("hello", "hello"))

    def test_outputs_match_with_trailing_whitespace(self):
        """Outputs should match despite trailing whitespace."""
        self.assertTrue(outputs_match("hello  \n", "hello"))
        self.assertTrue(outputs_match("hello\n\n", "hello"))

    def test_outputs_match_different(self):
        """Different outputs should not match."""
        self.assertFalse(outputs_match("hello", "world"))


class SyntaxCheckTests(TestCase):
    """Tests for Python syntax checking."""

    def test_valid_syntax(self):
        """Valid Python code should pass syntax check."""
        code = """
def hello():
    return "world"
print(hello())
"""
        is_valid, error = check_syntax(code)
        self.assertTrue(is_valid)
        self.assertEqual(error, '')

    def test_invalid_syntax_missing_colon(self):
        """Missing colon should be caught."""
        code = """
def hello()
    return "world"
"""
        is_valid, error = check_syntax(code)
        self.assertFalse(is_valid)
        self.assertIn("Line", error)

    def test_invalid_syntax_bad_indent(self):
        """Bad indentation should be caught."""
        code = """
def hello():
return "world"
"""
        is_valid, error = check_syntax(code)
        self.assertFalse(is_valid)


class RunnerTests(TestCase):
    """Tests for the code runner."""

    def test_simple_print(self):
        """Simple print statement should work."""
        code = 'print("hello")'
        result = run_python_code(code, "")
        self.assertEqual(result.stdout.strip(), "hello")
        self.assertEqual(result.exit_code, 0)
        self.assertFalse(result.timed_out)

    def test_stdin_input(self):
        """Reading from stdin should work."""
        code = """
name = input()
print(f"Hello, {name}!")
"""
        result = run_python_code(code, "World")
        self.assertEqual(result.stdout.strip(), "Hello, World!")
        self.assertEqual(result.exit_code, 0)

    def test_runtime_error(self):
        """Runtime errors should be caught."""
        code = """
x = 1 / 0
"""
        result = run_python_code(code, "")
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("ZeroDivisionError", result.stderr)

    def test_timeout(self):
        """Long-running code should time out."""
        code = """
import time
time.sleep(10)
"""
        result = run_python_code(code, "", timeout=0.5)
        self.assertTrue(result.timed_out)

    def test_code_size_limit(self):
        """Oversized code should be rejected."""
        # Create code larger than MAX_CODE_BYTES (50KB)
        code = "x = " + "1" * 60000
        result = run_python_code(code, "")
        self.assertIsNotNone(result.error)
        self.assertIn("size limit", result.error)

    def test_execution_time_captured(self):
        """Execution time should be captured."""
        code = 'print("test")'
        result = run_python_code(code, "")
        self.assertIsInstance(result.elapsed_ms, int)
        self.assertGreater(result.elapsed_ms, 0)


@pytest.mark.django_db
class JudgeStdinStdoutTests(TestCase):
    """Tests for stdin/stdout judge mode."""

    def setUp(self):
        """Create test problem and user."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.problem = Problem.objects.create(
            title='Add Two Numbers',
            slug='add-two-numbers',
            description='Add two numbers from input',
            difficulty=1,
            judge_mode=JudgeMode.STDIN_STDOUT,
            is_published=True
        )
        # Create a test case
        ProblemTestCase.objects.create(
            problem=self.problem,
            input_data="3 5",
            expected_output="8",
            display_input="3 5",
            display_output="8",
            is_sample=True
        )

    def test_accepted_submission(self):
        """Correct solution should get ACCEPTED verdict."""
        code = """
a, b = map(int, input().split())
print(a + b)
"""
        submission = Submission.objects.create(
            problem=self.problem,
            user=self.user,
            code=code
        )
        result = judge_stdin_stdout(submission)
        self.assertEqual(result.verdict, Verdict.ACCEPTED)
        self.assertEqual(len(result.test_results), 1)
        self.assertTrue(result.test_results[0].passed)

    def test_wrong_answer(self):
        """Incorrect output should get WRONG_ANSWER verdict."""
        code = """
a, b = map(int, input().split())
print(a * b)  # Wrong: multiplication instead of addition
"""
        submission = Submission.objects.create(
            problem=self.problem,
            user=self.user,
            code=code
        )
        result = judge_stdin_stdout(submission)
        self.assertEqual(result.verdict, Verdict.WRONG_ANSWER)

    def test_runtime_error(self):
        """Code with runtime error should get RE verdict."""
        code = """
x = 1 / 0
"""
        submission = Submission.objects.create(
            problem=self.problem,
            user=self.user,
            code=code
        )
        result = judge_stdin_stdout(submission)
        self.assertEqual(result.verdict, Verdict.RUNTIME_ERROR)

    def test_compile_error(self):
        """Syntax error should get CE verdict."""
        code = """
def broken
    print("hello")
"""
        submission = Submission.objects.create(
            problem=self.problem,
            user=self.user,
            code=code
        )
        result = judge_stdin_stdout(submission)
        self.assertEqual(result.verdict, Verdict.COMPILE_ERROR)

    def test_execution_time_in_result(self):
        """Judge result should include total execution time."""
        code = """
a, b = map(int, input().split())
print(a + b)
"""
        submission = Submission.objects.create(
            problem=self.problem,
            user=self.user,
            code=code
        )
        result = judge_stdin_stdout(submission)
        self.assertIsInstance(result.total_time_ms, int)
        self.assertGreaterEqual(result.total_time_ms, 0)


@pytest.mark.django_db
class SubmissionModelTests(TestCase):
    """Tests for the Submission model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.problem = Problem.objects.create(
            title='Test Problem',
            slug='test-problem',
            description='A test problem',
            difficulty=1,
            is_published=True
        )

    def test_submission_defaults(self):
        """Submission should have correct defaults."""
        submission = Submission.objects.create(
            problem=self.problem,
            user=self.user,
            code='print("hello")'
        )
        self.assertEqual(submission.status, SubmissionStatus.PENDING)
        self.assertEqual(submission.verdict, Verdict.PENDING)
        self.assertEqual(submission.language, 'python')
        self.assertEqual(submission.test_results, [])

    def test_submission_str(self):
        """Submission string representation should be descriptive."""
        submission = Submission.objects.create(
            problem=self.problem,
            user=self.user,
            code='print("hello")',
            verdict=Verdict.ACCEPTED
        )
        self.assertIn(str(submission.pk), str(submission))
        self.assertIn(self.problem.title, str(submission))

    def test_submission_execution_time_nullable(self):
        """execution_time_ms should be nullable for old submissions."""
        submission = Submission.objects.create(
            problem=self.problem,
            user=self.user,
            code='print("hello")'
        )
        self.assertIsNone(submission.execution_time_ms)
