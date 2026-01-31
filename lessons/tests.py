import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Course, Lesson
from problems.models import Problem


User = get_user_model()


class CourseModelTests(TestCase):
    """Tests for the Course model."""
    
    def test_course_str_published(self):
        """Course string representation shows published status."""
        course = Course.objects.create(
            title="Python Basics",
            is_published=True
        )
        assert str(course) == "Python Basics (Published)"
    
    def test_course_str_draft(self):
        """Course string representation shows draft status."""
        course = Course.objects.create(
            title="Advanced Topics",
            is_published=False
        )
        assert str(course) == "Advanced Topics (Draft)"
    
    def test_course_auto_slug(self):
        """Course generates slug from title if not provided."""
        course = Course.objects.create(title="My First Course")
        assert course.slug == "my-first-course"
    
    def test_course_custom_slug(self):
        """Course uses provided slug."""
        course = Course.objects.create(
            title="My Course",
            slug="custom-slug"
        )
        assert course.slug == "custom-slug"
    
    def test_course_lesson_count(self):
        """Course correctly counts its lessons."""
        course = Course.objects.create(title="Test Course")
        Lesson.objects.create(title="Lesson 1", course=course, content_markdown="Content")
        Lesson.objects.create(title="Lesson 2", course=course, content_markdown="Content")
        
        assert course.lesson_count() == 2
    
    def test_course_published_lessons(self):
        """Course.published_lessons returns only published lessons."""
        course = Course.objects.create(title="Test Course")
        Lesson.objects.create(
            title="Published", 
            course=course, 
            content_markdown="Content",
            is_published=True
        )
        Lesson.objects.create(
            title="Draft", 
            course=course, 
            content_markdown="Content",
            is_published=False
        )
        
        published = course.published_lessons()
        assert published.count() == 1
        assert published.first().title == "Published"


class LessonModelTests(TestCase):
    """Tests for the Lesson model."""
    
    def setUp(self):
        self.course = Course.objects.create(title="Test Course")
    
    def test_lesson_str_with_course(self):
        """Lesson string includes course name."""
        lesson = Lesson.objects.create(
            title="Variables",
            course=self.course,
            content_markdown="Content",
            is_published=True
        )
        assert str(lesson) == "Test Course / Variables (Published)"
    
    def test_lesson_str_standalone(self):
        """Standalone lesson string shows only title."""
        lesson = Lesson.objects.create(
            title="Standalone Lesson",
            content_markdown="Content",
            is_published=False
        )
        assert str(lesson) == "Standalone Lesson (Draft)"
    
    def test_lesson_auto_slug(self):
        """Lesson generates slug from title if not provided."""
        lesson = Lesson.objects.create(
            title="Introduction to Python",
            content_markdown="Content"
        )
        assert lesson.slug == "introduction-to-python"
    
    def test_lesson_navigation_next(self):
        """get_next_lesson returns the next published lesson."""
        lesson1 = Lesson.objects.create(
            title="Lesson 1",
            course=self.course,
            content_markdown="Content",
            order=1,
            is_published=True
        )
        lesson2 = Lesson.objects.create(
            title="Lesson 2",
            course=self.course,
            content_markdown="Content",
            order=2,
            is_published=True
        )
        
        assert lesson1.get_next_lesson() == lesson2
        assert lesson2.get_next_lesson() is None
    
    def test_lesson_navigation_previous(self):
        """get_previous_lesson returns the previous published lesson."""
        lesson1 = Lesson.objects.create(
            title="Lesson 1",
            course=self.course,
            content_markdown="Content",
            order=1,
            is_published=True
        )
        lesson2 = Lesson.objects.create(
            title="Lesson 2",
            course=self.course,
            content_markdown="Content",
            order=2,
            is_published=True
        )
        
        assert lesson2.get_previous_lesson() == lesson1
        assert lesson1.get_previous_lesson() is None
    
    def test_lesson_navigation_skips_drafts(self):
        """Navigation skips unpublished lessons."""
        lesson1 = Lesson.objects.create(
            title="Lesson 1",
            course=self.course,
            content_markdown="Content",
            order=1,
            is_published=True
        )
        Lesson.objects.create(
            title="Draft Lesson",
            course=self.course,
            content_markdown="Content",
            order=2,
            is_published=False
        )
        lesson3 = Lesson.objects.create(
            title="Lesson 3",
            course=self.course,
            content_markdown="Content",
            order=3,
            is_published=True
        )
        
        assert lesson1.get_next_lesson() == lesson3
    
    def test_lesson_standalone_no_navigation(self):
        """Standalone lessons (no course) have no navigation."""
        lesson = Lesson.objects.create(
            title="Standalone",
            content_markdown="Content",
            is_published=True
        )
        
        assert lesson.get_next_lesson() is None
        assert lesson.get_previous_lesson() is None


class LessonProblemLinkTests(TestCase):
    """Tests for linking problems to lessons."""
    
    def test_lesson_can_link_problems(self):
        """Lessons can be linked to multiple problems."""
        lesson = Lesson.objects.create(
            title="Arrays Intro",
            content_markdown="Content"
        )
        problem1 = Problem.objects.create(
            title="Two Sum",
            description="Find two numbers",
            difficulty=1
        )
        problem2 = Problem.objects.create(
            title="Three Sum",
            description="Find three numbers",
            difficulty=2
        )
        
        lesson.problems.add(problem1, problem2)
        
        assert lesson.problems.count() == 2
        assert problem1 in lesson.problems.all()
        assert problem2 in lesson.problems.all()
    
    def test_problem_can_access_related_lessons(self):
        """Problems can access lessons they're linked to."""
        lesson = Lesson.objects.create(
            title="Arrays Intro",
            content_markdown="Content"
        )
        problem = Problem.objects.create(
            title="Two Sum",
            description="Find two numbers",
            difficulty=1
        )
        
        lesson.problems.add(problem)
        
        assert lesson in problem.lessons.all()
