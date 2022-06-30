from django.db import models
from django.utils.translation import gettext_lazy as _

from .user import CustomUser


class Registration(models.Model):
    class UserRole(models.TextChoices):
        Student = 'Student'
        Instructor = 'Instructor'
        TA = 'TA'

    users = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    courses = models.ForeignKey('Course', on_delete=models.CASCADE)

    userRole = models.TextField(
        choices=UserRole.choices, default=UserRole.Student)

    class Meta:
        db_table = 'registration'
        verbose_name = _('registration')
        verbose_name_plural = _('registrations')
