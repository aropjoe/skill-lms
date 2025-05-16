from django.db import models
from courses.models import Lesson

class TextContent(models.Model):
    """Holds textual content for a lesson."""
    lesson = models.ForeignKey(
        Lesson,
        related_name='text_content',
        on_delete=models.CASCADE,
        help_text="The lesson this text content is part of."
    )
    body = models.TextField(help_text="The main text content.")
    order = models.PositiveIntegerField(
        default=0,
        help_text="Order of this content block within the lesson."
    )

    class Meta:
        verbose_name_plural = "Text Content"
        ordering = ['order']

    def __str__(self):
        return f"Text content for {self.lesson.title} ({self.body[:50]}...)"

class ImageContent(models.Model):
    """Holds image assets for a lesson."""
    lesson = models.ForeignKey(
        Lesson,
        related_name='image_content',
        on_delete=models.CASCADE,
        help_text="The lesson this image content is part of."
    )
    image = models.ImageField(
        upload_to='lesson_images/',
        help_text="The image file."
    )
    caption = models.CharField(
        max_length=255,
        blank=True,
        help_text="A caption for the image."
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Order of this content block within the lesson."
    )

    class Meta:
        verbose_name_plural = "Image Content"
        ordering = ['order']

    def __str__(self):
        return f"Image content for {self.lesson.title} ({self.image.name})"

class VideoContent(models.Model):
    """Holds embedded video content for a lesson."""
    lesson = models.ForeignKey(
        Lesson,
        related_name='video_content',
        on_delete=models.CASCADE,
        help_text="The lesson this video content is part of."
    )
    video_url = models.URLField(help_text="URL of the embedded video (e.g., YouTube link).")
    caption = models.CharField(
        max_length=255,
        blank=True,
        help_text="A caption for the video."
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Order of this content block within the lesson."
    )

    class Meta:
        verbose_name_plural = "Video Content"
        ordering = ['order']

    def __str__(self):
        return f"Video content for {self.lesson.title} ({self.video_url})"

class FileContent(models.Model):
    """Holds downloadable file assets for a lesson (Optional)."""
    lesson = models.ForeignKey(
        Lesson,
        related_name='file_content',
        on_delete=models.CASCADE,
        help_text="The lesson this file content is part of."
    )
    file = models.FileField(
        upload_to='lesson_files/',
        help_text="The downloadable file."
    )
    title = models.CharField(max_length=200, help_text="Title of the file.")
    order = models.PositiveIntegerField(
        default=0,
        help_text="Order of this content block within the lesson."
    )

    class Meta:
        verbose_name_plural = "File Content"
        ordering = ['order']

    def __str__(self):
        return f"File content for {self.lesson.title} ({self.title})"