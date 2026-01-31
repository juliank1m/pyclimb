import markdown
from django.views import generic
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, JsonResponse
from django.urls import reverse_lazy, reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from .models import Course, Lesson
from .forms import CourseForm, LessonForm


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


# =============================================================================
# Teacher Dashboard Views (Staff Only)
# =============================================================================

@method_decorator(staff_member_required, name='dispatch')
class TeachDashboardView(generic.TemplateView):
    """
    Staff dashboard for managing courses and lessons.
    """
    template_name = 'lessons/teach/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all().prefetch_related('lessons').order_by('order', 'title')
        context['standalone_lessons'] = Lesson.objects.filter(course__isnull=True).order_by('order', 'title')
        context['recent_lessons'] = Lesson.objects.all().order_by('-updated_at')[:10]
        return context


@method_decorator(staff_member_required, name='dispatch')
class CourseCreateView(generic.CreateView):
    """Create a new course."""
    model = Course
    form_class = CourseForm
    template_name = 'lessons/teach/course_form.html'
    
    def get_success_url(self):
        messages.success(self.request, f'Course "{self.object.title}" created successfully.')
        return reverse('lessons:teach_dashboard')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Create New Course'
        context['submit_text'] = 'Create Course'
        return context


@method_decorator(staff_member_required, name='dispatch')
class CourseUpdateView(generic.UpdateView):
    """Edit an existing course."""
    model = Course
    form_class = CourseForm
    template_name = 'lessons/teach/course_form.html'
    slug_url_kwarg = 'course_slug'
    
    def get_success_url(self):
        messages.success(self.request, f'Course "{self.object.title}" updated successfully.')
        return reverse('lessons:teach_dashboard')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'Edit Course: {self.object.title}'
        context['submit_text'] = 'Save Changes'
        context['course'] = self.object
        return context


@method_decorator(staff_member_required, name='dispatch')
class CourseDeleteView(generic.DeleteView):
    """Delete a course."""
    model = Course
    template_name = 'lessons/teach/course_confirm_delete.html'
    slug_url_kwarg = 'course_slug'
    success_url = reverse_lazy('lessons:teach_dashboard')
    
    def form_valid(self, form):
        messages.success(self.request, f'Course "{self.object.title}" deleted.')
        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class LessonCreateView(generic.CreateView):
    """Create a new lesson."""
    model = Lesson
    form_class = LessonForm
    template_name = 'lessons/teach/lesson_form.html'
    
    def get_initial(self):
        initial = super().get_initial()
        # Pre-select course if provided in URL
        course_slug = self.request.GET.get('course')
        if course_slug:
            try:
                course = Course.objects.get(slug=course_slug)
                initial['course'] = course
            except Course.DoesNotExist:
                pass
        return initial
    
    def get_success_url(self):
        messages.success(self.request, f'Lesson "{self.object.title}" created successfully.')
        return reverse('lessons:teach_dashboard')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Create New Lesson'
        context['submit_text'] = 'Create Lesson'
        return context


@method_decorator(staff_member_required, name='dispatch')
class LessonUpdateView(generic.UpdateView):
    """Edit an existing lesson."""
    model = Lesson
    form_class = LessonForm
    template_name = 'lessons/teach/lesson_form.html'
    slug_url_kwarg = 'lesson_slug'
    
    def get_success_url(self):
        messages.success(self.request, f'Lesson "{self.object.title}" updated successfully.')
        return reverse('lessons:teach_dashboard')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'Edit Lesson: {self.object.title}'
        context['submit_text'] = 'Save Changes'
        context['lesson'] = self.object
        return context


@method_decorator(staff_member_required, name='dispatch')
class LessonDeleteView(generic.DeleteView):
    """Delete a lesson."""
    model = Lesson
    template_name = 'lessons/teach/lesson_confirm_delete.html'
    slug_url_kwarg = 'lesson_slug'
    success_url = reverse_lazy('lessons:teach_dashboard')
    
    def form_valid(self, form):
        messages.success(self.request, f'Lesson "{self.object.title}" deleted.')
        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class LessonPreviewView(generic.DetailView):
    """Preview a lesson with rendered markdown."""
    model = Lesson
    template_name = 'lessons/teach/lesson_preview.html'
    slug_url_kwarg = 'lesson_slug'
    context_object_name = 'lesson'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content_html'] = render_markdown(self.object.content_markdown)
        return context


@staff_member_required
def lesson_toggle_publish(request, lesson_slug):
    """Toggle the published status of a lesson."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    lesson = get_object_or_404(Lesson, slug=lesson_slug)
    lesson.is_published = not lesson.is_published
    lesson.save()
    
    status = 'published' if lesson.is_published else 'unpublished'
    messages.success(request, f'Lesson "{lesson.title}" is now {status}.')
    
    # Return to referrer or dashboard
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or reverse('lessons:teach_dashboard')
    return redirect(next_url)


@staff_member_required
def course_toggle_publish(request, course_slug):
    """Toggle the published status of a course."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    course = get_object_or_404(Course, slug=course_slug)
    course.is_published = not course.is_published
    course.save()
    
    status = 'published' if course.is_published else 'unpublished'
    messages.success(request, f'Course "{course.title}" is now {status}.')
    
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or reverse('lessons:teach_dashboard')
    return redirect(next_url)


@staff_member_required
def markdown_preview_api(request):
    """API endpoint for live markdown preview."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    content = request.POST.get('content', '')
    html = render_markdown(content)
    return JsonResponse({'html': html})


@staff_member_required
def image_upload(request):
    """Handle image uploads for lesson content."""
    import os
    import uuid
    from django.conf import settings
    from django.core.files.storage import default_storage
    
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    if 'image' not in request.FILES:
        return JsonResponse({'error': 'No image provided'}, status=400)
    
    image = request.FILES['image']
    
    # Validate file type
    allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
    if image.content_type not in allowed_types:
        return JsonResponse({
            'error': f'Invalid file type. Allowed: JPEG, PNG, GIF, WebP'
        }, status=400)
    
    # Validate file size (max 5MB)
    max_size = 5 * 1024 * 1024
    if image.size > max_size:
        return JsonResponse({
            'error': 'Image too large. Maximum size is 5MB.'
        }, status=400)
    
    # Generate unique filename
    ext = os.path.splitext(image.name)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
        ext = '.png'
    filename = f"lessons/{uuid.uuid4().hex}{ext}"
    
    # Save file
    path = default_storage.save(filename, image)
    url = default_storage.url(path)
    
    return JsonResponse({
        'url': url,
        'filename': os.path.basename(path)
    })
