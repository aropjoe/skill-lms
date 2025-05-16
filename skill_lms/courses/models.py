from django.db import models
from django.template.defaultfilters import slugify

class Course(models.Model):
    """Represents a distinct course offering in the LMS."""
    title = models.CharField(max_length=200, help_text="Title of the course.")
    slug = models.SlugField(unique=True, max_length=200, help_text="URL-friendly identifier for the course.")
    description = models.TextField(blank=True, help_text="Brief overview of the course.")
    image = models.ImageField(
        upload_to='course_images/',
        blank=True,
        null=True,
        help_text="Thumbnail or banner image for the course."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Courses"
        ordering = ['title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Module(models.Model):
    """Organizes lessons into logical groups within a course."""
    course = models.ForeignKey(
        Course,
        related_name='modules',
        on_delete=models.CASCADE,
        help_text="The course this module belongs to."
    )
    title = models.CharField(max_length=200, help_text="Title of the module.")
    description = models.TextField(blank=True, help_text="Brief description of the module.")
    order = models.PositiveIntegerField(
        default=0,
        help_text="The order of this module within the course."
    )

    class Meta:
        verbose_name_plural = "Modules"
        ordering = ['order']

    def __str__(self):
        return f"{self.order}: {self.title}"

class Lesson(models.Model):
    """Represents an individual unit of learning content within a module."""
    module = models.ForeignKey(
        Module,
        related_name='lessons',
        on_delete=models.CASCADE,
        help_text="The module this lesson belongs to."
    )
    title = models.CharField(max_length=200, help_text="Title of the lesson.")
    slug = models.SlugField(max_length=200, help_text="URL-friendly identifier for the lesson.")
    order = models.PositiveIntegerField(
        default=0,
        help_text="The order of this lesson within the module."
    )

    class Meta:
        verbose_name_plural = "Lessons"
        ordering = ['order']
        unique_together = ('module', 'slug')

    def __str__(self):
        return f"{self.order}: {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)