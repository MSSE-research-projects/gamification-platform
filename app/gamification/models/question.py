from django.db import models


class Question(models.Model):
    """
    Model for Question
    """
    class Question_type(models.TextChoices):
        TEXT = 'TEXT'
        MULTIPLECHOICE = 'MULTIPLECHOICE'

    section = models.ForeignKey('SurveySection', on_delete=models.CASCADE)

    name = models.CharField(max_length=150)

    text = models.TextField(blank=True)

    is_required = models.BooleanField(default=False)

    question_type = models.TextChoices(
        choice=Question_type.choices, default=Question_type.TEXT)

    class Meta:
        db_table = 'question'
        verbose_name = 'question'
        verbose_name_plural = 'questions'
