from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone

DIFFICULTY_CHOICES = [
    (1, "Easy"),
    (2, "Medium"),
    (3, "Hard"),
]


class Problem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    constraints = models.TextField(blank=True)
    follow_up = models.TextField(blank=True)
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES)

    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.get_difficulty_display()})"

class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='test_cases')

    input_data = models.TextField(
        help_text="Raw stdin passed to the user's program"
    )
    expected_output = models.TextField(
        help_text="Exact stdout expected from the program"
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
    