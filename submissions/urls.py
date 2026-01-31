from django.urls import path
from . import views

app_name = 'submissions'

urlpatterns = [
    path('create/<slug:problem_slug>/', views.create_submission, name='create'),
    path('<int:pk>/', views.SubmissionDetailView.as_view(), name='detail'),
]
