from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('modules/<int:module_id>/lessons_tabbed/', views.module_detail_with_lessons_view, name='module_lessons_tabbed'),
    path('<slug:course_slug>/', views.course_detail, name='course_detail'),
    path('<slug:course_slug>/<slug:lesson_slug>/', views.lesson_detail, name='lesson_detail'),
]
