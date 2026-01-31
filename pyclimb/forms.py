"""
Custom forms for the pyclimb project.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    """Extended registration form with email field."""
    email = forms.EmailField(
        required=False,
        help_text='Optional. Used for password reset and notifications.'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
