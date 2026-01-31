from django.contrib import admin
from django import forms
from .models import Submission


class SubmissionAdminForm(forms.ModelForm):
    """Custom form to style the code textarea."""
    class Meta:
        model = Submission
        fields = '__all__'
        widgets = {
            'code': forms.Textarea(attrs={
                'rows': 20,
                'style': 'font-family: monospace; font-size: 14px; width: 100%;',
            }),
            'stdout': forms.Textarea(attrs={
                'rows': 8,
                'style': 'font-family: monospace; font-size: 13px; width: 100%;',
            }),
            'stderr': forms.Textarea(attrs={
                'rows': 8,
                'style': 'font-family: monospace; font-size: 13px; width: 100%;',
            }),
        }


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    form = SubmissionAdminForm
    list_display = ['id', 'problem', 'user', 'language', 'status', 'verdict', 'created_at']
    list_filter = ['status', 'verdict', 'language']
    search_fields = ['problem__title', 'user__username']
    readonly_fields = ['created_at']
    ordering = ['-created_at']

    fieldsets = [
        (None, {
            'fields': ['problem', 'user', 'language']
        }),
        ('Code', {
            'fields': ['code'],
        }),
        ('Execution', {
            'fields': ['status', 'verdict', 'stdout', 'stderr'],
        }),
        ('Metadata', {
            'fields': ['created_at'],
            'classes': ['collapse'],
        }),
    ]

    class Media:
        js = ('admin/js/tab_support.js',)
