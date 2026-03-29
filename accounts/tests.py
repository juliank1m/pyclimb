"""
Tests for the accounts app.

Focuses on:
- UserProfile creation
- User registration
"""
import pytest
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from accounts.models import UserProfile


@pytest.mark.django_db
class UserProfileTests(TestCase):
    """Tests for UserProfile model."""

    def test_profile_created_on_user_creation(self):
        """UserProfile should be created automatically with new users."""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.assertTrue(hasattr(user, 'profile'))
        self.assertIsInstance(user.profile, UserProfile)

    def test_profile_defaults(self):
        """New profile should have correct defaults."""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        profile = user.profile
        self.assertFalse(profile.is_verified)
        self.assertEqual(profile.verification_token, '')

    def test_generate_verification_token(self):
        """generate_verification_token should create a unique token."""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        profile = user.profile
        token = profile.generate_verification_token()
        self.assertIsNotNone(token)
        self.assertTrue(len(token) > 20)
        self.assertEqual(profile.verification_token, token)

    def test_verify_method(self):
        """verify() should mark profile as verified."""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        profile = user.profile
        profile.generate_verification_token()
        profile.verify()
        self.assertTrue(profile.is_verified)
        self.assertEqual(profile.verification_token, '')

    def test_profile_str(self):
        """Profile string should include username."""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.assertIn('testuser', str(user.profile))


@pytest.mark.django_db
class RegistrationTests(TestCase):
    """Tests for user registration."""

    def setUp(self):
        self.client = Client()

    def test_registration_creates_user(self):
        """Registration should create a new user."""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
        })
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_registration_creates_profile(self):
        """Registration should create a UserProfile."""
        self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
        })
        user = User.objects.get(username='newuser')
        self.assertTrue(hasattr(user, 'profile'))

    def test_registration_logs_in_user(self):
        """Registration should automatically log in the user."""
        self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
        })
        # Check session indicates logged in
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
