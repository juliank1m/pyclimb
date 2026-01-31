from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ['is_verified', 'verification_token']
    readonly_fields = ['verification_token']


class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]


# Re-register User with the new admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
