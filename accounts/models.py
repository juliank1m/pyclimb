"""
User profile model for email verification.
"""
import secrets
from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    """Extended user profile with email verification status."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    is_verified = models.BooleanField(
        default=False,
        help_text="Whether the user's email has been verified"
    )
    verification_token = models.CharField(
        max_length=64,
        blank=True,
        help_text="Token for email verification"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile for {self.user.username}"

    def generate_verification_token(self):
        """Generate a new verification token."""
        self.verification_token = secrets.token_urlsafe(32)
        self.save(update_fields=['verification_token'])
        return self.verification_token

    def verify(self):
        """Mark the email as verified."""
        self.is_verified = True
        self.verification_token = ''
        self.save(update_fields=['is_verified', 'verification_token'])
