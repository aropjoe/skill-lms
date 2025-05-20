from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Course, Module, Lesson
from content.models import TextContent, ImageContent, VideoContent, FileContent
#from django.views.decorators.csrf import csrf_exempt


def module_detail_with_lessons_view(request, module_id):
    """
    Displays a module with all its lessons and their content in a tabbed interface.
    Fetches lessons and all related content blocks for each lesson.
    """
    # Fetch the module object
    module = get_object_or_404(Module, id=module_id)

    # Fetch all lessons related to this module, ordered by their order field
    lessons = module.lessons.all().order_by('order')

    # Prepare data structure to hold lessons and their combined content
    lessons_data = []

    # Iterate through each lesson to fetch its content
    for lesson in lessons:
        # Fetch all content blocks related to this specific lesson from each content model
        text_blocks = lesson.text_content.all() # Uses related_name='text_content'
        image_blocks = lesson.image_content.all() # Uses related_name='image_content'
        video_blocks = lesson.video_content.all() # Uses related_name='video_content'
        file_blocks = lesson.file_content.all() # Uses related_name='file_content'

        # Combine all content blocks into a single list
        all_content_for_lesson = sorted(
            list(text_blocks) + list(image_blocks) + list(video_blocks) + list(file_blocks),
            key=lambda content_block: content_block.order # Sort by the 'order' field
        )

        # Append the lesson object and its sorted content to the lessons_data list
        lessons_data.append({
            'lesson_obj': lesson,
            'contents': all_content_for_lesson
        })

    # Prepare the context dictionary to pass data to the template
    context = {
        'module': module, # Pass the module object
        'lessons_data': lessons_data, # Pass the list of lessons with their content
        'current_module_id': module_id, # Useful for JS or highlighting current module
    }

    # Render the template, passing the context
    return render(request, 'courses/module_detail_with_lessons_view.html', context) # Assuming template is in courses/


def course_list(request):
    """
    Displays a list of all available courses.
    """
    courses = Course.objects.all().order_by('title')
    return render(request, 'courses/course_list.html', {'courses': courses})


def course_detail(request, course_slug):
    """
    Displays details of a single course, including its modules and lessons.
    """
    course = get_object_or_404(Course, slug=course_slug)

    modules = course.modules.all().order_by('order')

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'modules': modules,
    })


def lesson_detail(request, course_slug, lesson_slug):
    """
    Displays the content of a single lesson.
    """

    lesson = get_object_or_404(
        Lesson,
        slug=lesson_slug,
        module__course__slug=course_slug
    )

    text_blocks = lesson.text_content.all()
    image_blocks = lesson.image_content.all()
    video_blocks = lesson.video_content.all()
    file_blocks = lesson.file_content.all()

    all_content = sorted(
        list(text_blocks) + list(image_blocks) + list(video_blocks) + list(file_blocks),
        key=lambda content_block: content_block.order
    )

    return render(request, 'courses/lesson_detail.html', {
        'lesson': lesson,
        'all_content': all_content,
    })
