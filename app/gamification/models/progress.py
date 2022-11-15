from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class Progress(models.Model):
    cur_point = models.FloatField(null=True, blank=True)
    point = models.ForeignKey('Point', on_delete=models.CASCADE)
    student = models.ForeignKey('Registration', on_delete=models.CASCADE)

    class Meta:
        db_table = 'progresses'
        verbose_name = _('progress')
        verbose_name_plural = _('progresses')

