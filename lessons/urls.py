from django.urls import path
from . import views

app_name = 'lessons'

urlpatterns = [
    # Public learning routes
    path('', views.LearnIndexView.as_view(), name='index'),
    
    # Teacher dashboard routes (staff only) - under /learn/teach/
    path('teach/', views.TeachDashboardView.as_view(), name='teach_dashboard'),
    path('teach/course/new/', views.CourseCreateView.as_view(), name='course_create'),
    path('teach/course/<slug:course_slug>/edit/', views.CourseUpdateView.as_view(), name='course_edit'),
    path('teach/course/<slug:course_slug>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),
    path('teach/course/<slug:course_slug>/toggle-publish/', views.course_toggle_publish, name='course_toggle_publish'),
    path('teach/lesson/new/', views.LessonCreateView.as_view(), name='lesson_create'),
    path('teach/lesson/<slug:lesson_slug>/edit/', views.LessonUpdateView.as_view(), name='lesson_edit'),
    path('teach/lesson/<slug:lesson_slug>/delete/', views.LessonDeleteView.as_view(), name='lesson_delete'),
    path('teach/lesson/<slug:lesson_slug>/preview/', views.LessonPreviewView.as_view(), name='lesson_preview'),
    path('teach/lesson/<slug:lesson_slug>/toggle-publish/', views.lesson_toggle_publish, name='lesson_toggle_publish'),
    path('teach/api/markdown-preview/', views.markdown_preview_api, name='markdown_preview_api'),
    
    # Public course/lesson routes (must be after teach/ routes)
    path('<slug:course_slug>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('<slug:course_slug>/<slug:lesson_slug>/', views.LessonDetailView.as_view(), name='lesson_detail'),
]
