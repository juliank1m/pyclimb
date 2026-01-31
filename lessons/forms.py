from django import forms
from .models import Course, Lesson


class CourseForm(forms.ModelForm):
    """Form for creating and editing courses."""
    
    class Meta:
        model = Course
        fields = ['title', 'slug', 'description', 'order', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Course title',
                'autofocus': True,
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'course-slug (auto-generated if blank)',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 3,
                'placeholder': 'Brief description of what this course covers...',
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-input form-input-small',
                'min': 0,
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-checkbox',
            }),
        }
        help_texts = {
            'slug': 'URL-friendly identifier. Leave blank to auto-generate from title.',
            'order': 'Lower numbers appear first in the course list.',
            'is_published': 'Only published courses are visible to learners.',
        }


class LessonForm(forms.ModelForm):
    """Form for creating and editing lessons."""
    
    class Meta:
        model = Lesson
        fields = ['title', 'slug', 'course', 'summary', 'content_markdown', 'order', 'is_published', 'problems']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Lesson title',
                'autofocus': True,
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'lesson-slug (auto-generated if blank)',
            }),
            'course': forms.Select(attrs={
                'class': 'form-select',
            }),
            'summary': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Short description shown in lesson lists',
            }),
            'content_markdown': forms.Textarea(attrs={
                'class': 'form-textarea markdown-editor',
                'rows': 25,
                'placeholder': '# Lesson Title\n\nWrite your lesson content here using Markdown...\n\n## Section\n\nUse **bold** and *italic* text.\n\n```python\n# Code blocks are supported\nprint("Hello, world!")\n```',
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-input form-input-small',
                'min': 0,
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-checkbox',
            }),
            'problems': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-checkbox-list',
            }),
        }
        help_texts = {
            'slug': 'URL-friendly identifier. Leave blank to auto-generate from title.',
            'course': 'Assign to a course, or leave blank for a standalone lesson.',
            'summary': 'Appears in lesson lists. Keep it brief.',
            'content_markdown': 'Supports Markdown: # headings, **bold**, *italic*, `code`, ```python code blocks```, - lists, [links](url)',
            'order': 'Lower numbers appear first within the course.',
            'is_published': 'Only published lessons are visible to learners.',
            'problems': 'Link practice problems to this lesson.',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show published problems in the selection
        from problems.models import Problem
        self.fields['problems'].queryset = Problem.objects.filter(is_published=True).order_by('difficulty', 'title')
        self.fields['course'].queryset = Course.objects.all().order_by('order', 'title')
        self.fields['course'].empty_label = '— Standalone (no course) —'
