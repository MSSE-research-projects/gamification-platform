from re import T
from django.db import models

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
