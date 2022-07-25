from django.db import models
from django.utils.translation import gettext_lazy as _

# from .user import CustomUser
from .artifact import Artifact
from .registration import Registration

class ArtifactReview(models.Model):
    
    #TO-DO - consider about on_delete setting here
    artifact = models.ForeignKey(Artifact, on_delete=models.CASCADE)
    
    regisration = models.ForeignKey(Registration, on_delete=models.CASCADE)

    class Meta:
        db_table = 'artifact_review'
        verbose_name = _('artifact_review')
        verbose_name_plural = _('artifact_reviews')
