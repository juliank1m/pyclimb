from django.shortcuts import render
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
        
        # Show user's past submissions for this problem
        if self.request.user.is_authenticated:
            context['user_submissions'] = self.object.submissions.filter(
                user=self.request.user
            ).order_by('-created_at')[:5]
        
        return context
