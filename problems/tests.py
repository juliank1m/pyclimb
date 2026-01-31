"""
Tests for the problems app.

Focuses on:
- Model validation
- Tag functionality
- View behavior
"""
import pytest
from django.test import TestCase, Client
from django.urls import reverse

from problems.models import Problem, TestCase as ProblemTestCase, Tag, JudgeMode


@pytest.mark.django_db
class ProblemModelTests(TestCase):
    """Tests for the Problem model."""

    def test_slug_auto_generated(self):
        """Slug should be auto-generated from title."""
        problem = Problem.objects.create(
            title='Two Sum Problem',
            description='Find two numbers that add up to target',
            difficulty=1
        )
        self.assertEqual(problem.slug, 'two-sum-problem')

    def test_slug_not_overwritten(self):
        """Existing slug should not be overwritten."""
        problem = Problem.objects.create(
            title='Two Sum Problem',
            slug='custom-slug',
            description='Find two numbers',
            difficulty=1
        )
        self.assertEqual(problem.slug, 'custom-slug')

    def test_difficulty_choices(self):
        """Difficulty should display correct labels."""
        easy = Problem.objects.create(
            title='Easy Problem', description='', difficulty=1
        )
        medium = Problem.objects.create(
            title='Medium Problem', description='', difficulty=2
        )
        hard = Problem.objects.create(
            title='Hard Problem', description='', difficulty=3
        )
        self.assertEqual(easy.get_difficulty_display(), 'Easy')
        self.assertEqual(medium.get_difficulty_display(), 'Medium')
        self.assertEqual(hard.get_difficulty_display(), 'Hard')

    def test_sample_cases_method(self):
        """sample_cases() should return only sample test cases."""
        problem = Problem.objects.create(
            title='Test Problem',
            description='',
            difficulty=1
        )
        ProblemTestCase.objects.create(
            problem=problem,
            input_data='1',
            expected_output='1',
            display_input='1',
            display_output='1',
            is_sample=True
        )
        ProblemTestCase.objects.create(
            problem=problem,
            input_data='2',
            expected_output='2',
            is_sample=False
        )
        samples = problem.sample_cases()
        self.assertEqual(samples.count(), 1)

    def test_function_call_mode_requires_entrypoint(self):
        """Function-call mode should require entrypoint_name."""
        problem = Problem(
            title='Function Problem',
            description='',
            difficulty=1,
            judge_mode=JudgeMode.FUNCTION_CALL,
            entrypoint_name=''  # Missing entrypoint
        )
        with self.assertRaises(Exception):
            problem.full_clean()


@pytest.mark.django_db
class TagModelTests(TestCase):
    """Tests for the Tag model."""

    def test_tag_slug_auto_generated(self):
        """Tag slug should be auto-generated."""
        tag = Tag.objects.create(name='Dynamic Programming')
        self.assertEqual(tag.slug, 'dynamic-programming')

    def test_tag_str(self):
        """Tag string should be the name."""
        tag = Tag.objects.create(name='Arrays')
        self.assertEqual(str(tag), 'Arrays')

    def test_tag_ordering(self):
        """Tags should be ordered by name."""
        Tag.objects.create(name='Strings')
        Tag.objects.create(name='Arrays')
        Tag.objects.create(name='Hashing')
        tags = list(Tag.objects.all())
        self.assertEqual([t.name for t in tags], ['Arrays', 'Hashing', 'Strings'])


@pytest.mark.django_db
class ProblemTagsTests(TestCase):
    """Tests for Problem-Tag relationship."""

    def test_problem_can_have_multiple_tags(self):
        """A problem can have multiple tags."""
        problem = Problem.objects.create(
            title='Two Sum',
            description='',
            difficulty=1
        )
        tag1 = Tag.objects.create(name='Arrays')
        tag2 = Tag.objects.create(name='Hashing')
        problem.tags.add(tag1, tag2)
        self.assertEqual(problem.tags.count(), 2)

    def test_tag_can_have_multiple_problems(self):
        """A tag can be associated with multiple problems."""
        tag = Tag.objects.create(name='Arrays')
        p1 = Problem.objects.create(title='P1', description='', difficulty=1)
        p2 = Problem.objects.create(title='P2', description='', difficulty=2)
        p1.tags.add(tag)
        p2.tags.add(tag)
        self.assertEqual(tag.problems.count(), 2)


@pytest.mark.django_db
class ProblemViewTests(TestCase):
    """Tests for problem views."""

    def setUp(self):
        self.client = Client()
        self.problem = Problem.objects.create(
            title='Test Problem',
            slug='test-problem',
            description='A test problem',
            difficulty=1,
            is_published=True
        )

    def test_index_view_shows_published_problems(self):
        """Index view should show published problems."""
        response = self.client.get(reverse('problems:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Problem')

    def test_index_view_hides_unpublished_problems(self):
        """Index view should not show unpublished problems."""
        Problem.objects.create(
            title='Hidden Problem',
            slug='hidden-problem',
            description='',
            difficulty=1,
            is_published=False
        )
        response = self.client.get(reverse('problems:index'))
        self.assertNotContains(response, 'Hidden Problem')

    def test_detail_view_shows_problem(self):
        """Detail view should show problem details."""
        response = self.client.get(
            reverse('problems:detail', kwargs={'slug': 'test-problem'})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Problem')
        self.assertContains(response, 'A test problem')

    def test_detail_view_404_for_unpublished(self):
        """Detail view should 404 for unpublished problems."""
        Problem.objects.create(
            title='Hidden',
            slug='hidden',
            description='',
            difficulty=1,
            is_published=False
        )
        response = self.client.get(
            reverse('problems:detail', kwargs={'slug': 'hidden'})
        )
        self.assertEqual(response.status_code, 404)

    def test_filter_by_difficulty(self):
        """Index view should filter by difficulty."""
        Problem.objects.create(
            title='Hard Problem',
            slug='hard-problem',
            description='',
            difficulty=3,
            is_published=True
        )
        response = self.client.get(reverse('problems:index') + '?difficulty=3')
        self.assertContains(response, 'Hard Problem')
        self.assertNotContains(response, 'Test Problem')

    def test_filter_by_tag(self):
        """Index view should filter by tag."""
        tag = Tag.objects.create(name='Arrays')
        self.problem.tags.add(tag)
        
        Problem.objects.create(
            title='Other Problem',
            slug='other-problem',
            description='',
            difficulty=1,
            is_published=True
        )
        
        response = self.client.get(reverse('problems:index') + '?tag=arrays')
        self.assertContains(response, 'Test Problem')
        self.assertNotContains(response, 'Other Problem')
