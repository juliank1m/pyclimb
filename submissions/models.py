from django.db import models
from django.conf import settings
from problems.models import Problem


class SubmissionStatus(models.TextChoices):
    """Execution state of a submission."""
    PENDING = 'pending', 'Pending'
    RUNNING = 'running', 'Running'
    DONE = 'done', 'Done'


class Verdict(models.TextChoices):
    """Judge result after execution."""
    PENDING = 'pending', 'Pending'       # Not yet judged
    ACCEPTED = 'AC', 'Accepted'
    WRONG_ANSWER = 'WA', 'Wrong Answer'
    RUNTIME_ERROR = 'RE', 'Runtime Error'
    TIME_LIMIT = 'TLE', 'Time Limit Exceeded'
    COMPILE_ERROR = 'CE', 'Compilation Error'  # Syntax error for Python


class Submission(models.Model):
    """A user's code submission for a problem."""

    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='submissions'
    )

    code = models.TextField(
        help_text="The submitted source code"
    )
    language = models.CharField(
        max_length=20,
        default='python',
        help_text="Programming language (python only for MVP)"
    )

    # Execution state (tracks where we are in the pipeline)
    status = models.CharField(
        max_length=20,
        choices=SubmissionStatus.choices,
        default=SubmissionStatus.PENDING
    )

    # Judge result (what happened when we ran the code)
    verdict = models.CharField(
        max_length=20,
        choices=Verdict.choices,
        default=Verdict.PENDING
    )

    # Captured output for debugging
    stdout = models.TextField(
        blank=True,
        help_text="Captured standard output"
    )
    stderr = models.TextField(
        blank=True,
        help_text="Captured standard error"
    )

    # Per-test-case results (JSON array)
    # Each entry: {test_id, is_sample, passed, verdict, stdout, stderr, expected, input_display}
    test_results = models.JSONField(
        default=list,
        blank=True,
        help_text="Detailed results for each test case"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Submission {self.pk} for {self.problem.title} ({self.get_verdict_display()})"
