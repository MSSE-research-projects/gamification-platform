from atexit import register
from django.db import models
from django.utils.translation import gettext_lazy as _

from app.gamification.models.registration import Registration


class Group(models.Model):
    registration = models.ManyToManyField(Registration, through='Membership')

    class Meta:
        db_table = 'groups'
        verbose_name = _('group')
        verbose_name_plural = _('groups')

    # @property
    # def members(self):
    #     Registration.objects.filter(
    #         courses=self.pk, userRole=role).values_list('users', flat=True)


# class Assignment(models.Model):
#     group = models.ForeignKey(Group, on_delete=models.CASCADE)


class Individual(Group):

    class Meta():
        db_table = 'individuals'
        verbose_name = _('individual')
        verbose_name_plural = _('individuals')


class Team(Group):
    name = models.CharField(_('team'), max_length=150, blank=True)

    class Meta():
        db_table = 'teams'
        verbose_name = _('team')
        verbose_name_plural = _('teams')
