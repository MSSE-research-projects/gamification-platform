from django.db import models
from django.utils.translation import gettext_lazy as _

from .registration import Registration


class Membership(models.Model):
    student = models.ForeignKey(Registration, on_delete=models.CASCADE)

    group = models.ForeignKey('Group', on_delete=models.CASCADE)

    class Meta:
        db_table = 'membership'
        verbose_name = _('membership')
        verbose_name_plural = _('membership')
