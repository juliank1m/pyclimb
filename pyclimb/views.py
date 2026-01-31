from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Count, Q

from problems.models import Problem
from submissions.models import Submission, Verdict


def register(request):
    """Handle user registration."""
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    """Display user profile with stats."""
    user = request.user
    
    # Get submission stats
    submissions = Submission.objects.filter(user=user)
    total_submissions = submissions.count()
    
    # Count by verdict
    verdict_counts = submissions.values('verdict').annotate(count=Count('verdict'))
    verdict_stats = {v['verdict']: v['count'] for v in verdict_counts}
    
    # Get solved problems (problems with at least one AC)
    solved_problem_ids = submissions.filter(
        verdict=Verdict.ACCEPTED
    ).values_list('problem_id', flat=True).distinct()
    solved_count = len(set(solved_problem_ids))
    
    # Total published problems
    total_problems = Problem.objects.filter(is_published=True).count()
    
    # Recent submissions
    recent_submissions = submissions.select_related('problem').order_by('-created_at')[:10]
    
    # Solved problems by difficulty
    solved_problems = Problem.objects.filter(
        id__in=solved_problem_ids, is_published=True
    )
    easy_solved = solved_problems.filter(difficulty=1).count()
    medium_solved = solved_problems.filter(difficulty=2).count()
    hard_solved = solved_problems.filter(difficulty=3).count()
    
    # Total by difficulty
    total_easy = Problem.objects.filter(is_published=True, difficulty=1).count()
    total_medium = Problem.objects.filter(is_published=True, difficulty=2).count()
    total_hard = Problem.objects.filter(is_published=True, difficulty=3).count()
    
    context = {
        'total_submissions': total_submissions,
        'solved_count': solved_count,
        'total_problems': total_problems,
        'accepted_count': verdict_stats.get(Verdict.ACCEPTED, 0),
        'wrong_answer_count': verdict_stats.get(Verdict.WRONG_ANSWER, 0),
        'runtime_error_count': verdict_stats.get(Verdict.RUNTIME_ERROR, 0),
        'tle_count': verdict_stats.get(Verdict.TIME_LIMIT, 0),
        'recent_submissions': recent_submissions,
        'easy_solved': easy_solved,
        'medium_solved': medium_solved,
        'hard_solved': hard_solved,
        'total_easy': total_easy,
        'total_medium': total_medium,
        'total_hard': total_hard,
    }
    
    return render(request, 'registration/profile.html', context)
