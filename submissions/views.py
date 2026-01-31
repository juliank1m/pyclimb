from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic

from problems.models import Problem
from .models import Submission
from .forms import SubmissionForm
from .services.judge import run_judge


def create_submission(request, problem_slug):
    """Handle code submission for a problem."""
    problem = get_object_or_404(Problem, slug=problem_slug, is_published=True)

    if request.method == 'POST':
        form = SubmissionForm(request.POST, problem=problem)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.problem = problem
            # Attach user if authenticated (optional for MVP)
            if request.user.is_authenticated:
                submission.user = request.user
            submission.save()

            # Run the judge synchronously (MVP - no async queue)
            run_judge(submission)

            return redirect('submissions:detail', pk=submission.pk)
    else:
        form = SubmissionForm(problem=problem)

    return render(request, 'submissions/create.html', {
        'form': form,
        'problem': problem,
    })


class SubmissionDetailView(generic.DetailView):
    """Display submission result."""
    model = Submission
    template_name = 'submissions/detail.html'
    context_object_name = 'submission'
