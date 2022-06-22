from django.db import models
from django.utils.translation import gettext_lazy as _

from .user import CustomUser
from .registration import Registration


class Course(models.Model):

    course_id = models.CharField(_('course_id'), max_length=150, blank=True)

    course_name = models.CharField(
        _('course name'), max_length=150, blank=True)

    syllabus = models.TextField(_('syllabus'), blank=True)

    semester = models.CharField(_('semester'), max_length=150, blank=True)

    visible = models.BooleanField(_('visible'), default=False)

    users = models.ManyToManyField(CustomUser, through='Registration')

    class Meta:
        db_table = 'courses'
        verbose_name = _('course')
        verbose_name_plural = _('courses')

    @property
    def instructors(self):
        query = Registration.objects.filter(
            courses=self.pk, userRole=Registration.UserRole.Instructor).values_list('users', flat=True)
        return self.users.filter(pk__in=query)

    @property
    def students(self):
        query = Registration.objects.filter(
            courses=self.pk, userRole=Registration.UserRole.Student).values_list('users', flat=True)
        return self.users.filter(pk__in=query)

    @property
    def TAs(self):
        query = Registration.objects.filter(
            courses=self.pk, userRole=Registration.UserRole.TA).values_list('users', flat=True)
        return self.users.filter(pk__in=query)

    def get_course_name(self):
        '''Return the course name.'''
        return self.course_name
