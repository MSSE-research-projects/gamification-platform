from django.db import models
from django.utils.translation import gettext_lazy as _


class SurveySection(models.Model):
    """
    Model for SurveySection
    """
    name = models.CharField(max_length=150)

    template = models.ForeignKey('SurveyTemplate', on_delete=models.CASCADE)

    title = models.CharField(max_length=150)

    description = models.TextField(blank=True)

    is_required = models.BooleanField(default=False)

    class Meta:
        db_table = 'survey_section'
        verbose_name = _('survey section')
        verbose_name_plural = _('survey sections')

    @property
    def questions(self):
        # return self.question_set.all()
        pass

    def __str__(self):
        return self.title
