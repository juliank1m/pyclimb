from django.shortcuts import redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from .models import Submission


def create_submission(request, problem_slug):
    """Deprecated: redirect to combined problem + submission page."""
    url = reverse('problems:detail', kwargs={'slug': problem_slug})
    from_submission_id = request.GET.get('from_submission')
    if from_submission_id:
        url = f"{url}?from_submission={from_submission_id}"
    return redirect(url)


class SubmissionListView(LoginRequiredMixin, generic.ListView):
    """Display user's submission history."""
    model = Submission
    template_name = 'submissions/list.html'
    context_object_name = 'submissions'
    paginate_by = 20

    def get_queryset(self):
        """Only show submissions belonging to the current user."""
        queryset = Submission.objects.filter(user=self.request.user)
        
        # Optional filtering by problem
        problem_slug = self.request.GET.get('problem')
        if problem_slug:
            queryset = queryset.filter(problem__slug=problem_slug)
        
        # Optional filtering by verdict
        verdict = self.request.GET.get('verdict')
        if verdict:
            queryset = queryset.filter(verdict=verdict)
        
        return queryset.select_related('problem').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verdict_choices'] = Submission.verdict.field.choices
        context['current_problem'] = self.request.GET.get('problem', '')
        context['current_verdict'] = self.request.GET.get('verdict', '')
        return context


class SubmissionDetailView(generic.DetailView):
    """Display submission result."""
    model = Submission
    template_name = 'submissions/detail.html'
    context_object_name = 'submission'

    def get_object(self, queryset=None):
        """Ensure users can only view their own submissions."""
        obj = super().get_object(queryset)
        
        # Allow viewing if:
        # 1. User owns the submission
        # 2. Submission is anonymous (no user) - for backward compatibility
        if obj.user is not None:
            if not self.request.user.is_authenticated:
                raise Http404("Submission not found")
            if obj.user != self.request.user:
                raise Http404("Submission not found")
        
        return obj
