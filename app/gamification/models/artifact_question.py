from django.db import models


class ArtifactQuestion(models.Model):
    """
    Model for ArtifactQuestion
    """
    artifact = models.ForeignKey('Artifact', on_delete=models.CASCADE)

    page = models.IntegerField(default=0)

    class Meta:
        db_table = 'artifact_question'
        verbose_name = 'artifact question'
        verbose_name_plural = 'artifact questions'
