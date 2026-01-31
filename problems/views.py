from django.shortcuts import render
from django.views import generic
from .models import Problem


class IndexView(generic.ListView):
    template_name = "problems/index.html"
    context_object_name = "published_problem_list"
    
    def get_queryset(self):
        return Problem.objects.filter(is_published=True).order_by("pk")


class DetailView(generic.DetailView):
    model = Problem
    template_name = "problems/detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Problem.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Show user's past submissions for this problem
        if self.request.user.is_authenticated:
            context['user_submissions'] = self.object.submissions.filter(
                user=self.request.user
            ).order_by('-created_at')[:5]
        
        return context
