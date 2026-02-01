from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Count, Q, Sum, Case, When, IntegerField
from django.contrib import messages

from .forms import RegistrationForm
from accounts.models import UserProfile
from problems.models import Problem
from lessons.models import Course, Lesson
from submissions.models import Submission, Verdict
from submissions.services.sandbox import get_sandbox_status


def home(request):
    """Homepage with overview and featured problems."""
    # Get published problem counts by difficulty
    problems = Problem.objects.filter(is_published=True)
    total_problems = problems.count()
    easy_count = problems.filter(difficulty=1).count()
    medium_count = problems.filter(difficulty=2).count()
    hard_count = problems.filter(difficulty=3).count()
    
    # Get featured problems (a mix of difficulties, most recent)
    featured_problems = list(problems.order_by('-created_at')[:6])
    
    # User-specific stats
    solved_count = 0
    solved_problem_ids = set()
    if request.user.is_authenticated:
        solved_problem_ids = set(
            Submission.objects.filter(
                user=request.user,
                verdict=Verdict.ACCEPTED
            ).values_list('problem_id', flat=True).distinct()
        )
        solved_count = len(solved_problem_ids)
    
    # Total users and submissions for site stats
    total_users = User.objects.count()
    total_submissions = Submission.objects.count()
    
    # Learning content stats
    total_courses = Course.objects.filter(is_published=True).count()
    total_lessons = Lesson.objects.filter(is_published=True).count()
    
    context = {
        'total_problems': total_problems,
        'easy_count': easy_count,
        'medium_count': medium_count,
        'hard_count': hard_count,
        'featured_problems': featured_problems,
        'solved_count': solved_count,
        'solved_problem_ids': solved_problem_ids,
        'total_users': total_users,
        'total_submissions': total_submissions,
        'total_courses': total_courses,
        'total_lessons': total_lessons,
    }
    
    return render(request, 'home.html', context)


def send_verification_email(request, user, profile):
    """Send email verification link to user."""
    token = profile.generate_verification_token()
    verify_url = request.build_absolute_uri(f'/accounts/verify/{token}/')
    
    subject = 'Verify your PyClimb account'
    message = f"""Hi {user.username},

Thanks for registering on PyClimb!

Please click the link below to verify your email address:

{verify_url}

If you didn't create an account, you can ignore this email.

- The PyClimb Team
"""
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,  # Don't fail registration if email fails
        )
    except Exception:
        pass  # Email is best-effort


def register(request):
    """Handle user registration."""
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # Send verification email if user provided an email
            if user.email:
                try:
                    profile = user.profile
                    send_verification_email(request, user, profile)
                    messages.info(request, 'A verification email has been sent to your email address.')
                except UserProfile.DoesNotExist:
                    pass  # Profile not created yet (shouldn't happen with signal)
            
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = RegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})


def verify_email(request, token):
    """Handle email verification via token."""
    profile = get_object_or_404(UserProfile, verification_token=token)
    
    if profile.verification_token and profile.verification_token == token:
        profile.verify()
        messages.success(request, 'Your email has been verified successfully!')
        return redirect('profile')
    
    messages.error(request, 'Invalid or expired verification link.')
    return redirect('profile')


@login_required
def profile(request):
    """Display user profile with stats."""
    user = request.user
    
    # Get or create profile
    try:
        user_profile = user.profile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=user)
    
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
        'user_profile': user_profile,
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


@login_required
def resend_verification(request):
    """Resend verification email."""
    user = request.user
    
    if not user.email:
        messages.error(request, 'Please add an email address to your account first.')
        return redirect('profile')
    
    try:
        profile = user.profile
        if profile.is_verified:
            messages.info(request, 'Your email is already verified.')
        else:
            send_verification_email(request, user, profile)
            messages.success(request, 'Verification email sent!')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profile not found.')
    
    return redirect('profile')


def leaderboard(request):
    """Display leaderboard ranking users by problems solved."""
    # Get all users who have at least one accepted submission
    # Score = sum of difficulty weights (Easy=1, Medium=2, Hard=3) for distinct solved problems
    
    # Build the leaderboard data
    leaderboard_data = []
    
    # Get all users with at least one accepted submission
    users_with_submissions = User.objects.filter(
        submissions__verdict=Verdict.ACCEPTED
    ).distinct()
    
    for user in users_with_submissions:
        # Get distinct solved problems for this user
        solved_problem_ids = Submission.objects.filter(
            user=user,
            verdict=Verdict.ACCEPTED
        ).values_list('problem_id', flat=True).distinct()
        
        # Get the problems and calculate score
        solved_problems = Problem.objects.filter(
            id__in=solved_problem_ids,
            is_published=True
        )
        
        problems_solved = solved_problems.count()
        
        if problems_solved == 0:
            continue
        
        # Calculate weighted score
        easy_count = solved_problems.filter(difficulty=1).count()
        medium_count = solved_problems.filter(difficulty=2).count()
        hard_count = solved_problems.filter(difficulty=3).count()
        
        score = easy_count * 1 + medium_count * 2 + hard_count * 3
        
        leaderboard_data.append({
            'username': user.username,
            'problems_solved': problems_solved,
            'easy_count': easy_count,
            'medium_count': medium_count,
            'hard_count': hard_count,
            'score': score,
        })
    
    # Sort by score (descending), then by problems solved, then by username
    leaderboard_data.sort(key=lambda x: (-x['score'], -x['problems_solved'], x['username']))
    
    # Add ranks (handling ties)
    for i, entry in enumerate(leaderboard_data[:50], start=1):
        entry['rank'] = i
    
    context = {
        'leaderboard': leaderboard_data[:50],  # Top 50 users
        'total_problems': Problem.objects.filter(is_published=True).count(),
    }
    
    return render(request, 'leaderboard.html', context)


def privacy_policy(request):
    """Display privacy policy."""
    return render(request, 'legal/privacy.html')


def terms_of_service(request):
    """Display terms of service."""
    return render(request, 'legal/terms.html')


def cookie_policy(request):
    """Display cookie policy."""
    return render(request, 'legal/cookies.html')


def sandbox_status(request):
    """Health check for sandbox configuration."""
    return JsonResponse(get_sandbox_status())
