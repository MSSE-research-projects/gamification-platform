from django.db import models


class SurveyTemplate(models.Model):
    """
    Model for SurveyTemplate
    """
    name = models.CharField(max_length=150)

    instructions = models.TextField(blank=True)

    other_info = models.TextField(blank=True)

    class Meta:
        db_table = 'survey_template'
        verbose_name = 'survey template'
        verbose_name_plural = 'survey templates'

    def __str__(self):
        return self.name
