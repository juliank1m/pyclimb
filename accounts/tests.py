"""
Tests for the accounts app.

Focuses on:
- UserProfile creation
- Email verification flow
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
class EmailVerificationViewTests(TestCase):
    """Tests for email verification views."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_verify_with_valid_token(self):
        """Valid token should verify the user."""
        profile = self.user.profile
        token = profile.generate_verification_token()
        
        response = self.client.get(
            reverse('verify_email', kwargs={'token': token})
        )
        
        profile.refresh_from_db()
        self.assertTrue(profile.is_verified)
        # Redirects to profile, which then redirects to login (user not logged in)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('profile'))

    def test_verify_with_invalid_token(self):
        """Invalid token should return 404."""
        response = self.client.get(
            reverse('verify_email', kwargs={'token': 'invalid-token'})
        )
        self.assertEqual(response.status_code, 404)

    def test_resend_verification_requires_login(self):
        """Resend verification should require authentication."""
        response = self.client.get(reverse('resend_verification'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

    def test_resend_verification_logged_in(self):
        """Logged in user can resend verification."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('resend_verification'))
        self.assertRedirects(response, reverse('profile'))


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
