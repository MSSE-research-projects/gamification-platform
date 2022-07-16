from django.db import models


class SurveyQuestion(models.Model):
    """
    Model for SurveyQuestion
    """
    is_multiple = models.BooleanField(default=False)

    option_group = models.ForeignKey(
        'OptionGroup', on_delete=models.CASCADE, null=True, blank=True)

    dependent_question = models.ForeignKey(
        'Question', on_delete=models.CASCADE, null=True, blank=True)

    dependent_option = models.ForeignKey(
        'OptionChoice', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'survey_question'
        verbose_name = 'survey question'
        verbose_name_plural = 'survey questions'
