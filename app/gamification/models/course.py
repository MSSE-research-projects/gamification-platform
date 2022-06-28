from django.db import models
from django.utils.translation import gettext_lazy as _
from app.gamification.models.entity import Entity, Team

from app.gamification.models.membership import Membership

from .user import CustomUser
from .registration import Registration


class Course(models.Model):

    course_number = models.CharField(_('course_number'), max_length=150, blank=True)

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

    def get_query(self, role):
        return Registration.objects.filter(
            courses=self.pk, userRole=role).values_list('users', flat=True)

    @property
    def instructors(self):
        query = self.get_query(Registration.UserRole.Instructor)
        return self.users.filter(pk__in=query)

    @property
    def students(self):
        query = self.get_query(Registration.UserRole.Student)
        return self.users.filter(pk__in=query)

    @property
    def TAs(self):
        query = self.get_query(Registration.UserRole.TA)
        return self.users.filter(pk__in=query)

    @property
    def teams(self):
        query = Membership.objects.filter(
            student__in=Registration.objects.filter(
                courses=self.pk))
        s = set()
        for e in query:
            try:
                s.add(e.entity.team)
            except Team.DoesNotExist:
                pass
        return s

    def get_course_name(self):
        '''Return the course name.'''
        return self.course_name
