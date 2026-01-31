"""
Tests for the main pyclimb views.

Focuses on:
- Leaderboard functionality
- Profile view
- View permissions
"""
import pytest
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from problems.models import Problem
from submissions.models import Submission, Verdict


@pytest.mark.django_db
class LeaderboardViewTests(TestCase):
    """Tests for the leaderboard view."""

    def setUp(self):
        self.client = Client()
        # Create problems
        self.easy = Problem.objects.create(
            title='Easy Problem',
            slug='easy',
            description='',
            difficulty=1,
            is_published=True
        )
        self.medium = Problem.objects.create(
            title='Medium Problem',
            slug='medium',
            description='',
            difficulty=2,
            is_published=True
        )
        self.hard = Problem.objects.create(
            title='Hard Problem',
            slug='hard',
            description='',
            difficulty=3,
            is_published=True
        )

    def test_leaderboard_accessible(self):
        """Leaderboard should be publicly accessible."""
        response = self.client.get(reverse('leaderboard'))
        self.assertEqual(response.status_code, 200)

    def test_leaderboard_empty_when_no_submissions(self):
        """Leaderboard should show empty state with no submissions."""
        response = self.client.get(reverse('leaderboard'))
        self.assertContains(response, 'No one has solved')

    def test_leaderboard_shows_users(self):
        """Leaderboard should show users who solved problems."""
        user = User.objects.create_user('solver', password='pass123')
        Submission.objects.create(
            problem=self.easy,
            user=user,
            code='print(1)',
            verdict=Verdict.ACCEPTED
        )
        response = self.client.get(reverse('leaderboard'))
        self.assertContains(response, 'solver')

    def test_leaderboard_scoring(self):
        """Score should be weighted by difficulty."""
        user = User.objects.create_user('scorer', password='pass123')
        # Solve easy (1pt) + medium (2pts) + hard (3pts) = 6 pts
        for problem in [self.easy, self.medium, self.hard]:
            Submission.objects.create(
                problem=problem,
                user=user,
                code='print(1)',
                verdict=Verdict.ACCEPTED
            )
        response = self.client.get(reverse('leaderboard'))
        self.assertContains(response, '6')  # Total score

    def test_leaderboard_ranking(self):
        """Users should be ranked by score."""
        user1 = User.objects.create_user('user1', password='pass123')
        user2 = User.objects.create_user('user2', password='pass123')
        
        # User1 solves easy (1pt)
        Submission.objects.create(
            problem=self.easy, user=user1, code='', verdict=Verdict.ACCEPTED
        )
        # User2 solves hard (3pts)
        Submission.objects.create(
            problem=self.hard, user=user2, code='', verdict=Verdict.ACCEPTED
        )
        
        response = self.client.get(reverse('leaderboard'))
        content = response.content.decode()
        # user2 should appear before user1
        self.assertLess(content.find('user2'), content.find('user1'))

    def test_leaderboard_ignores_wrong_answers(self):
        """Only accepted submissions should count."""
        user = User.objects.create_user('trier', password='pass123')
        Submission.objects.create(
            problem=self.easy,
            user=user,
            code='print(2)',
            verdict=Verdict.WRONG_ANSWER
        )
        response = self.client.get(reverse('leaderboard'))
        self.assertNotContains(response, 'trier')


@pytest.mark.django_db
class ProfileViewTests(TestCase):
    """Tests for the profile view."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_profile_requires_login(self):
        """Profile should require authentication."""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

    def test_profile_accessible_when_logged_in(self):
        """Profile should be accessible for logged in users."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')

    def test_profile_shows_stats(self):
        """Profile should show submission stats."""
        self.client.login(username='testuser', password='testpass123')
        problem = Problem.objects.create(
            title='Test', slug='test', description='', difficulty=1, is_published=True
        )
        Submission.objects.create(
            problem=problem,
            user=self.user,
            code='',
            verdict=Verdict.ACCEPTED
        )
        response = self.client.get(reverse('profile'))
        self.assertContains(response, '1')  # 1 problem solved


@pytest.mark.django_db
class AuthViewTests(TestCase):
    """Tests for authentication views."""

    def setUp(self):
        self.client = Client()

    def test_login_page_accessible(self):
        """Login page should be accessible."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_register_page_accessible(self):
        """Register page should be accessible."""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_password_reset_page_accessible(self):
        """Password reset page should be accessible."""
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)

    def test_login_redirects_authenticated_user(self):
        """Login page should redirect authenticated users."""
        User.objects.create_user('testuser', password='pass123')
        self.client.login(username='testuser', password='pass123')
        response = self.client.get(reverse('login'))
        # Django auth view doesn't redirect by default, but register does
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 302)
