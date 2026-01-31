from django.contrib import admin
from django import forms
from .models import Problem, TestCase, Tag
from django.db import models


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'problem_count']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

    def problem_count(self, obj):
        return obj.problems.count()
    problem_count.short_description = 'Problems'


class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 1
    fields = [
        'is_sample',
        'input_data',
        'expected_output',
        'display_input',
        'display_output',
        'explanation',
    ]
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 3, 'cols': 29})}
    }


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    inlines = [TestCaseInline]

    # List view configuration
    list_display = ['title', 'difficulty', 'judge_mode', 'tag_list', 'is_published', 'created_at']
    list_filter = ['difficulty', 'is_published', 'judge_mode', 'tags']
    list_editable = ['is_published']
    search_fields = ['title', 'description']
    ordering = ['-created_at']
    filter_horizontal = ['tags']

    # Detail view configuration
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = [
        (None, {
            'fields': ['title', 'slug', 'difficulty', 'tags', 'is_published']
        }),
        ('Content', {
            'fields': ['description', 'constraints', 'follow_up'],
            'description': 'The main problem content shown to users.'
        }),
        ('Judge Configuration', {
            'fields': ['judge_mode', 'entrypoint_type', 'entrypoint_name', 'signature_text', 'starter_code'],
            'description': (
                'For Standard I/O: leave entrypoint fields blank. '
                'For Function Call: specify the function/method name and optionally provide signature and starter code.'
            ),
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse'],
        }),
    ]

    def tag_list(self, obj):
        return ', '.join(t.name for t in obj.tags.all())
    tag_list.short_description = 'Tags'