from django.contrib import admin
from django import forms
from django.db import models
from .models import Course, Lesson


class LessonInline(admin.TabularInline):
    """Inline view of lessons within a course."""
    model = Lesson
    extra = 0
    fields = ['order', 'title', 'is_published', 'summary']
    readonly_fields = ['title']
    ordering = ['order']
    show_change_link = True
    
    def has_add_permission(self, request, obj=None):
        # Don't allow adding lessons inline; use the full form instead
        return False


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson_count', 'is_published', 'order', 'updated_at']
    list_filter = ['is_published']
    list_editable = ['is_published', 'order']
    search_fields = ['title', 'description']
    ordering = ['order', 'title']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']
    inlines = [LessonInline]
    
    fieldsets = [
        (None, {
            'fields': ['title', 'slug', 'description', 'is_published', 'order']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse'],
        }),
    ]
    
    def lesson_count(self, obj):
        return obj.lessons.count()
    lesson_count.short_description = 'Lessons'


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'is_published', 'problem_count', 'updated_at']
    list_filter = ['is_published', 'course']
    list_editable = ['is_published', 'order']
    search_fields = ['title', 'summary', 'content_markdown']
    ordering = ['course', 'order', 'title']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['problems']
    
    # Make the markdown textarea larger and monospace
    formfield_overrides = {
        models.TextField: {
            'widget': forms.Textarea(attrs={
                'rows': 30,
                'cols': 100,
                'style': 'font-family: monospace; font-size: 14px;'
            })
        }
    }
    
    fieldsets = [
        (None, {
            'fields': ['title', 'slug', 'course', 'order', 'is_published']
        }),
        ('Content', {
            'fields': ['summary', 'content_markdown'],
            'description': (
                'Write lesson content in Markdown format. '
                'Supports: # headings, **bold**, *italic*, `code`, ```python code blocks```, '
                '- lists, [links](url), > blockquotes'
            ),
        }),
        ('Related Problems', {
            'fields': ['problems'],
            'description': 'Link problems for learners to practice after reading the lesson.',
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse'],
        }),
    ]
    
    def problem_count(self, obj):
        return obj.problems.count()
    problem_count.short_description = 'Problems'
