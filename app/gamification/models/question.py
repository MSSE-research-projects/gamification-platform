from django.db import models

from app.gamification.models.option_choice import OptionChoice


class Question(models.Model):
    """
    Model for Question
    """
    class Question_type(models.TextChoices):
        TEXT = 'TEXT'
        MULTIPLECHOICE = 'MULTIPLECHOICE'

    section = models.ForeignKey('SurveySection', on_delete=models.CASCADE)

    text = models.TextField(blank=True)

    is_required = models.BooleanField(default=False)

    is_multiple = models.BooleanField(default=False)

    dependent_question = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)

    question_type = models.TextField(
        choices=Question_type.choices, default=Question_type.TEXT)

    option_choices = models.ManyToManyField(
        'OptionChoice', through='QuestionOption')

    class Meta:
        db_table = 'question'
        verbose_name = 'question'
        verbose_name_plural = 'questions'
