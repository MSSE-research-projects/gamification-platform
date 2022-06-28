from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from app.gamification.models.course import Course


class Assignment(models.Model):

    class AssigmentType(models.TextChoices):
        Individual = 'Individual'
        Team = 'Team'

    class SubmissionType(models.TextChoices):
        File = 'File'
        URL = 'URL'
        Text = 'Text'

    class ReviewerAssignPolicy(models.TextChoices):
        A = 'A'
        B = 'B'
        C = 'C'

    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    assignment_name = models.CharField(
        _('assignment name'), max_length=150, blank=True)

    description = models.TextField(_('description'), blank=True)

    assignment_type = models.TextField(
        choices=AssigmentType.choices, default=AssigmentType.Individual, blank=True)

    submission_type = models.TextField(
        choices=SubmissionType.choices, default=SubmissionType.File, blank=True)

    total_score = models.FloatField(null=True, blank=True)

    weight = models.FloatField(null=True, blank=True)

    date_created = models.DateTimeField(
        _('date created'), null=True, default=now, blank=True)

    date_released = models.DateTimeField(
        _('date_released'),  null=True, blank=True)

    date_due = models.DateTimeField(_('date_due'),  null=True, blank=True)

    review_assign_policy = models.TextField(
        choices=ReviewerAssignPolicy.choices, default=ReviewerAssignPolicy.A, blank=True)

    class Meta:
        db_table = 'assignment'
        verbose_name = _('assignment')
        verbose_name_plural = _('assignments')