import markdown
from django.views import generic
from django.shortcuts import get_object_or_404
from django.http import Http404
from .models import Course, Lesson


def render_markdown(content):
    """
    Render markdown content to safe HTML.
    
    Uses fenced code blocks and code highlighting for Python snippets.
    """
    md = markdown.Markdown(
        extensions=[
            'fenced_code',
            'codehilite',
            'tables',
            'toc',
            'nl2br',
        ],
        extension_configs={
            'codehilite': {
                'css_class': 'highlight',
                'guess_lang': False,
            }
        }
    )
    return md.convert(content)


class LearnIndexView(generic.TemplateView):
    """
    Landing page for the learning section.
    Shows published courses and standalone lessons.
    """
    template_name = 'lessons/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get published courses with their lesson counts
        context['courses'] = Course.objects.filter(
            is_published=True
        ).prefetch_related('lessons')
        
        # Get standalone published lessons (not in any course)
        context['standalone_lessons'] = Lesson.objects.filter(
            is_published=True,
            course__isnull=True
        )
        
        return context


class CourseDetailView(generic.DetailView):
    """
    Shows a course with its list of lessons.
    Staff can preview drafts.
    """
    model = Course
    template_name = 'lessons/course_detail.html'
    context_object_name = 'course'
    slug_url_kwarg = 'course_slug'
    
    def get_queryset(self):
        queryset = Course.objects.prefetch_related('lessons')
        
        # Staff can view drafts
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_published=True)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get lessons - staff sees all, others see only published
        if self.request.user.is_staff:
            context['lessons'] = self.object.lessons.all()
        else:
            context['lessons'] = self.object.published_lessons()
        
        return context


class LessonDetailView(generic.TemplateView):
    """
    Shows a single lesson with rendered markdown content.
    Staff can preview drafts.
    """
    template_name = 'lessons/lesson_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        course_slug = self.kwargs['course_slug']
        lesson_slug = self.kwargs['lesson_slug']
        
        # Get the course
        course_qs = Course.objects.all()
        if not self.request.user.is_staff:
            course_qs = course_qs.filter(is_published=True)
        
        course = get_object_or_404(course_qs, slug=course_slug)
        
        # Get the lesson
        lesson_qs = course.lessons.all()
        if not self.request.user.is_staff:
            lesson_qs = lesson_qs.filter(is_published=True)
        
        lesson = get_object_or_404(lesson_qs, slug=lesson_slug)
        
        context['course'] = course
        context['lesson'] = lesson
        context['content_html'] = render_markdown(lesson.content_markdown)
        
        # Navigation - only show published lessons to non-staff
        if self.request.user.is_staff:
            all_lessons = list(course.lessons.all())
        else:
            all_lessons = list(course.published_lessons())
        
        try:
            current_index = all_lessons.index(lesson)
            context['previous_lesson'] = all_lessons[current_index - 1] if current_index > 0 else None
            context['next_lesson'] = all_lessons[current_index + 1] if current_index < len(all_lessons) - 1 else None
        except (ValueError, IndexError):
            context['previous_lesson'] = None
            context['next_lesson'] = None
        
        # Get related problems
        context['problems'] = lesson.problems.filter(is_published=True)
        
        # For table of contents
        context['all_lessons'] = all_lessons
        
        return context
