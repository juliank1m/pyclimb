from django.urls import path
from . import views

app_name = 'lessons'

urlpatterns = [
    path('', views.LearnIndexView.as_view(), name='index'),
    path('<slug:course_slug>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('<slug:course_slug>/<slug:lesson_slug>/', views.LessonDetailView.as_view(), name='lesson_detail'),
]
