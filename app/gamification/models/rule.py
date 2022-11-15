from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from app.gamification.models.constraint import Constraint
from app.gamification.models.reward import Reward


class Rule(models.Model):
    default = models.BooleanField(default=False)
    name = models.CharField(
        _('Rule name'), max_length=150, blank=True)

    description = models.TextField(_('description'), blank=True)

    @property
    def constraints(self):
        return Constraint.objects.filter(Rule=self)

    @property
    def rewards(self):
        return Reward.objects.filter(Rule=self)

    class Meta:
        db_table = 'rules'
        verbose_name = _('rule')
        verbose_name_plural = _('rules')

    def __str__(self):
        return f'{self.name}'
