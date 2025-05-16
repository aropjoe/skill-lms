from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('signin/', views.signin_view, name='signin'),
    path('signout/', views.signout_view, name='signout'),
    path('take-course/<slug:course_slug>/', views.take_course_view, name='take_course'),
    path('my-courses/', views.my_courses_view, name="my_courses"),
    path('', views.dashboard_view, name="dashboard"),
]
