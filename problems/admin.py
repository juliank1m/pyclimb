from django.contrib import admin
from django import forms
from .models import Problem, TestCase
from django.db import models

class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 1
    formfield_overrides={
        models.TextField: {'widget': forms.Textarea(attrs={'rows':3, 'cols':29})}
    }


class ProblemAdmin(admin.ModelAdmin):
    inlines = [TestCaseInline]
    list_display = ['title', 'created_at', 'updated_at', 'is_published']
    list_filter = ['difficulty']
    search_fields = ['title']

admin.site.register(Problem, ProblemAdmin)