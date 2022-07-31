from django.db import models

class Answer(models.Model):
    """
    Model for Answer
    """
    artifact = models.ForeignKey('Artifact', on_delete=models.CASCADE)

    #registration = models.ForeignKey('Registration', on_delete=models.CASCADE)

    questionOption = models.ForeignKey('QuestionOption', on_delete=models.CASCADE)

    answerText = models.TextField(blank=True)

    class Meta:
        db_table = 'answer'
        verbose_name = 'answer'
        verbose_name_plural = 'answers'
