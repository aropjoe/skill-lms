# users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserCourse
from django.contrib import messages
from django.db import IntegrityError 
from courses.models import Course
from django.db.models import Count
from content.models import TextContent, ImageContent, VideoContent, FileContent


@login_required
def dashboard_view(request):
    """
    Displays the user dashboard with summary statistics and charts.
    Fetches data such as total users, courses, enrollments,
    and data for course enrollment and content type distribution charts.
    """
    total_users = User.objects.count()
    total_courses = Course.objects.count()
    total_enrollments = UserCourse.objects.count()

    courses_by_enrollment = Course.objects.annotate(
        enrollment_count=Count('enrollments')
    ).order_by('-enrollment_count')[:5]

    enrollment_chart_labels = [course.title for course in courses_by_enrollment]
    enrollment_chart_data = [course.enrollment_count for course in courses_by_enrollment]

    total_text_content = TextContent.objects.count()
    total_image_content = ImageContent.objects.count()
    total_video_content = VideoContent.objects.count()
    total_file_content = FileContent.objects.count() 

    content_chart_labels = ['Text', 'Images', 'Videos', 'Files']
    content_chart_data = [
        total_text_content,
        total_image_content,
        total_video_content,
        total_file_content
    ]

    context = {
        'total_users': total_users,
        'total_courses': total_courses,
        'total_enrollments': total_enrollments,
        'enrollment_chart_labels': enrollment_chart_labels,
        'enrollment_chart_data': enrollment_chart_data,
        'content_chart_labels': content_chart_labels,
        'content_chart_data': content_chart_data,
    }
    return render(request, 'users/dashboard.html', context)


def signup_view(request):
    """
    Handles user registration. 
    """
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST.get('email', '')
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')

            if not username or not password:
                return render(request, 'users/signup.html', {
                    'error': 'Username and password are required.',
                    'form_data': request.POST
                }, status=400)

            if User.objects.filter(username=username).exists():
                 return render(request, 'users/signup.html', {
                    'error': 'Username already taken.',
                    'form_data': request.POST
                }, status=400)

            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            login(request, user)

            messages.success(request, 'Account created successfully! You are now logged in.')


            return redirect('courses:course_list')

        except KeyError as e:
            messages.error(request, f'An unexpected error occurred: {e}.')
            return render(request, 'users/signup.html', {
                'error': f'Missing required field: {e}.',
                'form_data': request.POST
            }, status=400)
        except Exception as e:
            return render(request, 'users/signup.html', {
                'error': f'An unexpected error occurred: {e}.',
                'form_data': request.POST
            }, status=500)

    else:
        return render(request, 'users/signup.html', {})

def signin_view(request):
    """
    Handles user login.
    """
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('courses:course_list')
            else:
                messages.error(request, 'Invalid username or password.')
                return render(request, 'users/signin.html', {
                    'error': 'Invalid username or password.',
                    'form_data': request.POST
                }, status=401)

        except KeyError as e:
            return render(request, 'users/signin.html', {
                'error': f'Missing required field: {e}.',
                'form_data': request.POST
            }, status=400)
        except Exception as e:
            return render(request, 'users/signin.html', {
                'error': f'An unexpected error occurred: {e}.',
                'form_data': request.POST
            }, status=500)

    else:
        return render(request, 'users/signin.html', {})


def signout_view(request):
    """
    Logs out the current user.
    """
    logout(request)
    messages.info(request, 'You have been signed out.')
    return redirect('users:signin')


@login_required
def take_course_view(request, course_slug):
    """
    A user taking a course by creating a UserCourse enrollment record.
    """
    if request.method == 'POST':
        course = get_object_or_404(Course, slug=course_slug)

        try:
            user_course = UserCourse.objects.create(user=request.user, course=course)
            print(f"User '{request.user.username}' successfully enrolled in course '{course.title}'.")
            messages.success(request, f'You are now enrolled in: {course.title}')

        except IntegrityError:
            print(f"User '{request.user.username}' is already enrolled in course '{course.title}'.")
            messages.info(request, f'You are already enrolled in the course: {course.title}')
            pass

        except Exception as e:
            print(f"An error occurred during enrollment for user '{request.user.username}' in course '{course.title}': {e}")
            messages.error(request, f'An error occurred while trying to enroll: {e}')

        return redirect('courses:course_detail', course_slug=course.slug)

    else:
        messages.warning(request, "Invalid request method for this action.")
        try:
             course = get_object_or_404(Course, slug=course_slug)
             return redirect('courses:course_detail', course_slug=course.slug)
        except:
             return redirect('courses:course_list')


@login_required
def my_courses_view(request):
    """
    Displays a list of courses the currently logged-in user is enrolled in.
    """
    user_enrollments = UserCourse.objects.filter(user=request.user).select_related('course')
    enrolled_courses = [enrollment.course for enrollment in user_enrollments]
    return render(request, 'users/my_courses.html', {'enrolled_courses': enrolled_courses})
