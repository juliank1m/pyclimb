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

