from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.views import generic
from .models import Problem, Tag, DIFFICULTY_CHOICES


class IndexView(generic.ListView):
    template_name = "problems/index.html"
    context_object_name = "published_problem_list"
    
    def get_queryset(self):
        queryset = Problem.objects.filter(is_published=True).prefetch_related('tags')
        
        # Filter by difficulty
        difficulty = self.request.GET.get('difficulty')
        if difficulty and difficulty.isdigit():
            queryset = queryset.filter(difficulty=int(difficulty))
        
        # Filter by tag
        tag_slug = self.request.GET.get('tag')
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)
        
        # Filter by solved status (requires auth)
        status = self.request.GET.get('status')
        if status and self.request.user.is_authenticated:
            from submissions.models import Verdict
            solved_ids = self.request.user.submissions.filter(
                verdict=Verdict.ACCEPTED
            ).values_list('problem_id', flat=True).distinct()
            
            if status == 'solved':
                queryset = queryset.filter(id__in=solved_ids)
            elif status == 'unsolved':
                queryset = queryset.exclude(id__in=solved_ids)
        
        return queryset.distinct().order_by('difficulty', 'pk')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['difficulty_choices'] = DIFFICULTY_CHOICES
        context['current_difficulty'] = self.request.GET.get('difficulty', '')
        context['current_status'] = self.request.GET.get('status', '')
        context['current_tag'] = self.request.GET.get('tag', '')
        
        # Get all tags that have at least one published problem
        context['available_tags'] = Tag.objects.filter(
            problems__is_published=True
        ).distinct().order_by('name')
        
        # Get solved problem IDs for the current user
        if self.request.user.is_authenticated:
            from submissions.models import Verdict
            context['solved_problem_ids'] = set(
                self.request.user.submissions.filter(
                    verdict=Verdict.ACCEPTED
                ).values_list('problem_id', flat=True).distinct()
            )
        else:
            context['solved_problem_ids'] = set()
        
        return context


class DetailView(generic.DetailView):
    model = Problem
    template_name = "problems/detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Problem.objects.filter(is_published=True).prefetch_related('tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        
        # Show user's past submissions for this problem
        if request.user.is_authenticated:
            context['user_submissions'] = self.object.submissions.filter(
                user=request.user
            ).order_by('-created_at')[:5]

        if 'form' not in context:
            from submissions.forms import SubmissionForm
            initial = {}
            from_submission_id = request.GET.get('from_submission')
            if from_submission_id:
                from submissions.models import Submission
                from_submission = get_object_or_404(Submission, pk=from_submission_id)
                if from_submission.problem_id != self.object.id:
                    from django.http import Http404
                    raise Http404("Submission not found")
                if from_submission.user is not None:
                    if not request.user.is_authenticated or from_submission.user != request.user:
                        from django.http import Http404
                        raise Http404("Submission not found")
                initial['code'] = from_submission.code
            context['form'] = SubmissionForm(problem=self.object, initial=initial)
        
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not getattr(settings, 'SUBMISSIONS_ENABLED', True):
            messages.error(request, 'Submissions are disabled in this environment.')
            return redirect('problems:detail', slug=self.object.slug)

        from submissions.services.runner import get_secure_execution_status
        secure_status = get_secure_execution_status()
        if secure_status['required'] and not secure_status['active']:
            messages.error(
                request,
                secure_status['reason'] or (
                    'Submissions are disabled because secure sandboxed '
                    'execution is not available on this deployment.'
                )
            )
            return redirect('problems:detail', slug=self.object.slug)

        from submissions.forms import SubmissionForm
        form = SubmissionForm(request.POST, problem=self.object)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.problem = self.object
            if request.user.is_authenticated:
                submission.user = request.user
            submission.save()

            from submissions.services.judge import run_judge
            run_judge(submission)

            return redirect('submissions:detail', pk=submission.pk)

        context = self.get_context_data(form=form)
        return render(request, self.template_name, context)
