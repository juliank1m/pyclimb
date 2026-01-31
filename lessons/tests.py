import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Course, Lesson
from problems.models import Problem


User = get_user_model()


class LearnIndexViewTests(TestCase):
    """Tests for the learn index page."""
    
    def setUp(self):
        self.client = Client()
    
    def test_index_shows_published_courses(self):
        """Published courses appear on the index page."""
        Course.objects.create(title="Published Course", is_published=True)
        Course.objects.create(title="Draft Course", is_published=False)
        
        response = self.client.get(reverse('lessons:index'))
        
        assert response.status_code == 200
        assert 'Published Course' in response.content.decode()
        assert 'Draft Course' not in response.content.decode()
    
    def test_index_shows_standalone_lessons(self):
        """Published standalone lessons appear on the index page."""
        Lesson.objects.create(
            title="Standalone Lesson",
            content_markdown="Content",
            is_published=True
        )
        
        response = self.client.get(reverse('lessons:index'))
        
        assert response.status_code == 200
        assert 'Standalone Lesson' in response.content.decode()
    
    def test_empty_index(self):
        """Empty state message when no content."""
        response = self.client.get(reverse('lessons:index'))
        
        assert response.status_code == 200
        assert 'No lessons available' in response.content.decode()


class CourseDetailViewTests(TestCase):
    """Tests for course detail page."""
    
    def setUp(self):
        self.client = Client()
        self.course = Course.objects.create(
            title="Python Basics",
            slug="python-basics",
            is_published=True
        )
        self.lesson = Lesson.objects.create(
            title="Variables",
            slug="variables",
            course=self.course,
            content_markdown="# Variables\n\nLearn about variables.",
            is_published=True
        )
    
    def test_published_course_accessible(self):
        """Published courses are accessible."""
        response = self.client.get(
            reverse('lessons:course_detail', args=['python-basics'])
        )
        
        assert response.status_code == 200
        assert 'Python Basics' in response.content.decode()
        assert 'Variables' in response.content.decode()
    
    def test_draft_course_404_for_anonymous(self):
        """Draft courses return 404 for anonymous users."""
        draft_course = Course.objects.create(
            title="Draft Course",
            slug="draft-course",
            is_published=False
        )
        
        response = self.client.get(
            reverse('lessons:course_detail', args=['draft-course'])
        )
        
        assert response.status_code == 404
    
    def test_draft_course_visible_to_staff(self):
        """Staff can view draft courses."""
        staff_user = User.objects.create_user(
            username='staff',
            password='testpass',
            is_staff=True
        )
        draft_course = Course.objects.create(
            title="Draft Course",
            slug="draft-course",
            is_published=False
        )
        
        self.client.login(username='staff', password='testpass')
        response = self.client.get(
            reverse('lessons:course_detail', args=['draft-course'])
        )
        
        assert response.status_code == 200
        assert 'Draft Course' in response.content.decode()


class LessonDetailViewTests(TestCase):
    """Tests for lesson detail page."""
    
    def setUp(self):
        self.client = Client()
        self.course = Course.objects.create(
            title="Python Basics",
            slug="python-basics",
            is_published=True
        )
        self.lesson = Lesson.objects.create(
            title="Variables",
            slug="variables",
            course=self.course,
            content_markdown="# Variables\n\nLearn about **variables** in Python.\n\n```python\nx = 5\n```",
            is_published=True
        )
    
    def test_lesson_renders_markdown(self):
        """Lesson content is rendered as HTML."""
        response = self.client.get(
            reverse('lessons:lesson_detail', args=['python-basics', 'variables'])
        )
        
        assert response.status_code == 200
        content = response.content.decode()
        # Check markdown was rendered
        assert '<strong>variables</strong>' in content or '<b>variables</b>' in content.lower()
    
    def test_draft_lesson_404_for_anonymous(self):
        """Draft lessons return 404 for anonymous users."""
        draft_lesson = Lesson.objects.create(
            title="Draft Lesson",
            slug="draft-lesson",
            course=self.course,
            content_markdown="Draft content",
            is_published=False
        )
        
        response = self.client.get(
            reverse('lessons:lesson_detail', args=['python-basics', 'draft-lesson'])
        )
        
        assert response.status_code == 404
    
    def test_lesson_shows_linked_problems(self):
        """Linked problems appear on lesson page."""
        problem = Problem.objects.create(
            title="Practice Problem",
            description="Practice",
            difficulty=1,
            is_published=True
        )
        self.lesson.problems.add(problem)
        
        response = self.client.get(
            reverse('lessons:lesson_detail', args=['python-basics', 'variables'])
        )
        
        assert response.status_code == 200
        assert 'Practice Problem' in response.content.decode()
    
    def test_lesson_navigation(self):
        """Prev/next navigation appears."""
        lesson2 = Lesson.objects.create(
            title="Functions",
            slug="functions",
            course=self.course,
            content_markdown="Functions content",
            order=2,
            is_published=True
        )
        self.lesson.order = 1
        self.lesson.save()
        
        # Check lesson 1 has "next" link
        response = self.client.get(
            reverse('lessons:lesson_detail', args=['python-basics', 'variables'])
        )
        assert 'Functions' in response.content.decode()
        
        # Check lesson 2 has "previous" link
        response = self.client.get(
            reverse('lessons:lesson_detail', args=['python-basics', 'functions'])
        )
        assert 'Variables' in response.content.decode()


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


# =============================================================================
# Teacher Dashboard Tests
# =============================================================================

class TeachDashboardViewTests(TestCase):
    """Tests for the teacher dashboard."""
    
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username='teacher',
            password='testpass',
            is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username='student',
            password='testpass',
            is_staff=False
        )
    
    def test_dashboard_requires_staff(self):
        """Non-staff users are redirected to login."""
        response = self.client.get(reverse('lessons:teach_dashboard'))
        assert response.status_code == 302
        assert '/admin/login/' in response.url
    
    def test_dashboard_accessible_to_staff(self):
        """Staff users can access the dashboard."""
        self.client.login(username='teacher', password='testpass')
        response = self.client.get(reverse('lessons:teach_dashboard'))
        assert response.status_code == 200
        assert 'Teacher Dashboard' in response.content.decode()
    
    def test_dashboard_shows_courses(self):
        """Dashboard displays all courses."""
        self.client.login(username='teacher', password='testpass')
        Course.objects.create(title="Test Course", is_published=True)
        
        response = self.client.get(reverse('lessons:teach_dashboard'))
        
        assert response.status_code == 200
        assert 'Test Course' in response.content.decode()


class CourseCreateViewTests(TestCase):
    """Tests for creating courses."""
    
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username='teacher',
            password='testpass',
            is_staff=True
        )
    
    def test_create_course_requires_staff(self):
        """Non-staff cannot access course creation."""
        response = self.client.get(reverse('lessons:course_create'))
        assert response.status_code == 302
    
    def test_create_course_form_renders(self):
        """Course creation form renders for staff."""
        self.client.login(username='teacher', password='testpass')
        response = self.client.get(reverse('lessons:course_create'))
        
        assert response.status_code == 200
        assert 'Create New Course' in response.content.decode()
    
    def test_create_course_success(self):
        """Staff can create a new course."""
        self.client.login(username='teacher', password='testpass')
        
        response = self.client.post(reverse('lessons:course_create'), {
            'title': 'New Course',
            'description': 'A test course',
            'order': 0,
        })
        
        assert response.status_code == 302  # Redirect on success
        assert Course.objects.filter(title='New Course').exists()


class LessonCreateViewTests(TestCase):
    """Tests for creating lessons."""
    
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username='teacher',
            password='testpass',
            is_staff=True
        )
        self.course = Course.objects.create(title="Test Course")
    
    def test_create_lesson_requires_staff(self):
        """Non-staff cannot access lesson creation."""
        response = self.client.get(reverse('lessons:lesson_create'))
        assert response.status_code == 302
    
    def test_create_lesson_form_renders(self):
        """Lesson creation form renders for staff."""
        self.client.login(username='teacher', password='testpass')
        response = self.client.get(reverse('lessons:lesson_create'))
        
        assert response.status_code == 200
        assert 'Create New Lesson' in response.content.decode()
    
    def test_create_lesson_success(self):
        """Staff can create a new lesson."""
        self.client.login(username='teacher', password='testpass')
        
        response = self.client.post(reverse('lessons:lesson_create'), {
            'title': 'New Lesson',
            'content_markdown': '# Hello\n\nThis is a test lesson.',
            'order': 0,
            'course': self.course.pk,
        })
        
        assert response.status_code == 302  # Redirect on success
        assert Lesson.objects.filter(title='New Lesson').exists()
    
    def test_create_lesson_preselects_course(self):
        """Course is preselected when provided in URL."""
        self.client.login(username='teacher', password='testpass')
        
        response = self.client.get(
            reverse('lessons:lesson_create') + f'?course={self.course.slug}'
        )
        
        assert response.status_code == 200


class LessonEditViewTests(TestCase):
    """Tests for editing lessons."""
    
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username='teacher',
            password='testpass',
            is_staff=True
        )
        self.lesson = Lesson.objects.create(
            title="Test Lesson",
            slug="test-lesson",
            content_markdown="Original content"
        )
    
    def test_edit_lesson_requires_staff(self):
        """Non-staff cannot edit lessons."""
        response = self.client.get(
            reverse('lessons:lesson_edit', args=['test-lesson'])
        )
        assert response.status_code == 302
    
    def test_edit_lesson_form_renders(self):
        """Lesson edit form renders with existing content."""
        self.client.login(username='teacher', password='testpass')
        response = self.client.get(
            reverse('lessons:lesson_edit', args=['test-lesson'])
        )
        
        assert response.status_code == 200
        assert 'Edit Lesson' in response.content.decode()
        assert 'Original content' in response.content.decode()
    
    def test_edit_lesson_success(self):
        """Staff can update a lesson."""
        self.client.login(username='teacher', password='testpass')
        
        response = self.client.post(
            reverse('lessons:lesson_edit', args=['test-lesson']),
            {
                'title': 'Updated Title',
                'slug': 'test-lesson',
                'content_markdown': 'Updated content',
                'order': 0,
            }
        )
        
        assert response.status_code == 302  # Redirect on success
        self.lesson.refresh_from_db()
        assert self.lesson.title == 'Updated Title'
        assert self.lesson.content_markdown == 'Updated content'


class LessonTogglePublishTests(TestCase):
    """Tests for toggling lesson publish status."""
    
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username='teacher',
            password='testpass',
            is_staff=True
        )
        self.lesson = Lesson.objects.create(
            title="Test Lesson",
            slug="test-lesson",
            content_markdown="Content",
            is_published=False
        )
    
    def test_toggle_requires_staff(self):
        """Non-staff cannot toggle publish status."""
        response = self.client.post(
            reverse('lessons:lesson_toggle_publish', args=['test-lesson'])
        )
        assert response.status_code == 302
        assert '/admin/login/' in response.url
    
    def test_toggle_publish(self):
        """Staff can toggle lesson from draft to published."""
        self.client.login(username='teacher', password='testpass')
        
        assert self.lesson.is_published is False
        
        response = self.client.post(
            reverse('lessons:lesson_toggle_publish', args=['test-lesson'])
        )
        
        assert response.status_code == 302  # Redirect
        self.lesson.refresh_from_db()
        assert self.lesson.is_published is True
    
    def test_toggle_unpublish(self):
        """Staff can toggle lesson from published to draft."""
        self.client.login(username='teacher', password='testpass')
        self.lesson.is_published = True
        self.lesson.save()
        
        response = self.client.post(
            reverse('lessons:lesson_toggle_publish', args=['test-lesson'])
        )
        
        self.lesson.refresh_from_db()
        assert self.lesson.is_published is False


class LessonPreviewViewTests(TestCase):
    """Tests for lesson preview."""
    
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username='teacher',
            password='testpass',
            is_staff=True
        )
        self.lesson = Lesson.objects.create(
            title="Test Lesson",
            slug="test-lesson",
            content_markdown="# Hello\n\nThis is **bold** text."
        )
    
    def test_preview_requires_staff(self):
        """Non-staff cannot access preview."""
        response = self.client.get(
            reverse('lessons:lesson_preview', args=['test-lesson'])
        )
        assert response.status_code == 302
    
    def test_preview_renders_markdown(self):
        """Preview renders markdown to HTML."""
        self.client.login(username='teacher', password='testpass')
        response = self.client.get(
            reverse('lessons:lesson_preview', args=['test-lesson'])
        )
        
        assert response.status_code == 200
        content = response.content.decode()
        assert 'Preview Mode' in content
        assert '<strong>bold</strong>' in content or '<b>bold</b>' in content.lower()
