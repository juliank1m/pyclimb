import json
from django.db import models
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from django.utils import timezone

DIFFICULTY_CHOICES = [
    (1, "Easy"),
    (2, "Medium"),
    (3, "Hard"),
]


class JudgeMode(models.TextChoices):
    """How the judge executes and evaluates submissions."""
    STDIN_STDOUT = 'stdin', 'Standard I/O'
    FUNCTION_CALL = 'function', 'Function Call (LeetCode-style)'


class EntrypointType(models.TextChoices):
    """What the user implements for function-call mode."""
    FUNCTION = 'function', 'Bare Function'
    SOLUTION_CLASS = 'class', 'Solution Class'


class Problem(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField()
    constraints = models.TextField(blank=True)
    follow_up = models.TextField(blank=True)
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES)

    # Judge configuration
    judge_mode = models.CharField(
        max_length=20,
        choices=JudgeMode.choices,
        default=JudgeMode.STDIN_STDOUT,
        help_text="How submissions are executed and evaluated"
    )
    entrypoint_type = models.CharField(
        max_length=20,
        choices=EntrypointType.choices,
        default=EntrypointType.SOLUTION_CLASS,
        blank=True,
        help_text="For function-call mode: what the user implements"
    )
    entrypoint_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="For function-call mode: function/method name to call (e.g., 'twoSum')"
    )
    signature_text = models.CharField(
        max_length=500,
        blank=True,
        help_text="Display signature shown to users (e.g., 'def twoSum(nums: list[int], target: int) -> list[int]')"
    )
    starter_code = models.TextField(
        blank=True,
        help_text="Template code pre-filled in the editor for users"
    )

    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.get_difficulty_display()})"

    def clean(self):
        """Validate judge configuration."""
        super().clean()
        if self.judge_mode == JudgeMode.FUNCTION_CALL:
            errors = {}
            if not self.entrypoint_name:
                errors['entrypoint_name'] = 'Function-call mode requires an entrypoint name.'
            if errors:
                raise ValidationError(errors)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def sample_cases(self):
        """Returns test cases marked as samples (visible to users)."""
        return self.test_cases.filter(is_sample=True)

class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='test_cases')

    input_data = models.TextField(
        help_text=(
            "For stdin mode: raw text passed to stdin. "
            "For function-call mode: JSON object of arguments (e.g., {\"nums\": [1,2], \"target\": 3})"
        )
    )
    expected_output = models.TextField(
        help_text=(
            "For stdin mode: exact stdout expected. "
            "For function-call mode: JSON value of expected return (e.g., [0,1])"
        )
    )
    
    display_input = models.TextField(
        blank=True,
        help_text="Human-readable version of the input (shown to users)"
    )
    display_output = models.TextField(
        blank=True,
        help_text="Human-readable version of the output (shown to users)"
    )
    explanation = models.TextField(
        blank=True,
        help_text="Optional explanation for this example"
    )

    is_sample = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """Validate test case data based on problem's judge mode."""
        super().clean()
        errors = {}

        # Sample test cases must have display fields
        if self.is_sample:
            if not self.display_input:
                errors['display_input'] = 'Sample test cases must have a display input.'
            if not self.display_output:
                errors['display_output'] = 'Sample test cases must have a display output.'

        # Function-call mode requires valid JSON
        if self.problem and self.problem.judge_mode == JudgeMode.FUNCTION_CALL:
            # Validate input_data is valid JSON (should be object or array)
            try:
                input_parsed = json.loads(self.input_data)
                if not isinstance(input_parsed, (dict, list)):
                    errors['input_data'] = (
                        'For function-call mode, input must be a JSON object '
                        '(e.g., {"nums": [1,2], "target": 3}) or array.'
                    )
            except json.JSONDecodeError as e:
                errors['input_data'] = f'Invalid JSON: {e.msg} at position {e.pos}'

            # Validate expected_output is valid JSON (any JSON value is OK)
            try:
                json.loads(self.expected_output)
            except json.JSONDecodeError as e:
                errors['expected_output'] = f'Invalid JSON: {e.msg} at position {e.pos}'

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"TestCase {self.pk} for {self.problem_id}"