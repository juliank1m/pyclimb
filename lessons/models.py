from django.db import models
from django.template.defaultfilters import slugify
from problems.models import Problem


class Course(models.Model):
    """A collection of lessons organized into a learning path."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(
        blank=True,
        help_text="Brief description of what this course covers"
    )
    is_published = models.BooleanField(
        default=False,
        help_text="Only published courses are visible to learners"
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order on the courses list (lower = first)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        status = "Published" if self.is_published else "Draft"
        return f"{self.title} ({status})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def published_lessons(self):
        """Returns only published lessons for this course."""
        return self.lessons.filter(is_published=True)

    def lesson_count(self):
        """Returns the total number of lessons in this course."""
        return self.lessons.count()


class Lesson(models.Model):
    """An individual lesson containing markdown content."""
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        null=True,
        blank=True,
        help_text="Optional: assign to a course for organized learning paths"
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    summary = models.CharField(
        max_length=500,
        blank=True,
        help_text="Short description shown in lesson lists"
    )
    content_markdown = models.TextField(
        help_text="Lesson content in Markdown format. Supports headings, lists, code blocks, links, etc."
    )
    
    # Navigation ordering
    order = models.PositiveIntegerField(
        default=0,
        help_text="Order within the course (lower = first)"
    )
    
    # Publishing
    is_published = models.BooleanField(
        default=False,
        help_text="Only published lessons are visible to learners"
    )
    
    # Related problems for practice
    problems = models.ManyToManyField(
        Problem,
        blank=True,
        related_name='lessons',
        help_text="Problems related to this lesson for practice"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['course', 'order', 'title']

    def __str__(self):
        status = "Published" if self.is_published else "Draft"
        if self.course:
            return f"{self.course.title} / {self.title} ({status})"
        return f"{self.title} ({status})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_next_lesson(self):
        """Returns the next lesson in the same course, or None."""
        if not self.course:
            return None
        return self.course.lessons.filter(
            is_published=True,
            order__gt=self.order
        ).first()

    def get_previous_lesson(self):
        """Returns the previous lesson in the same course, or None."""
        if not self.course:
            return None
        return self.course.lessons.filter(
            is_published=True,
            order__lt=self.order
        ).order_by('-order').first()
