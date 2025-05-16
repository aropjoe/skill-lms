from django.db import models
from django.contrib.auth.models import User
from courses.models import Course 


class UserCourse(models.Model):
    """Represents a user's enrollment in a specific course."""
    user = models.ForeignKey(
        User,
        related_name='enrolled_courses',
        on_delete=models.CASCADE,
        help_text="The user who is enrolled."
    )
    course = models.ForeignKey(
        Course,
        related_name='enrollments',
        on_delete=models.CASCADE,
        help_text="The course the user is enrolled in."
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')
        verbose_name_plural = "User Courses"
        ordering = ['enrolled_at']

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"

