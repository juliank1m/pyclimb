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

    def get_queryset(self):
        return Problem.objects.filter(is_published=True)
