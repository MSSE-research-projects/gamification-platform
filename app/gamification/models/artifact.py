from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator

from .entity import Entity
from .assignment import Assignment
from .feedback import Feedback
from .artifact_review import ArtifactReview
from app.gamification.models import artifact_review

class Artifact(models.Model):
    
    file_extension_validator = FileExtensionValidator(
        allowed_extensions=['png', 'jpg', 'jpeg', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt', 'zip',
                            'rar', '7z', 'gz', 'tar', 'bz2', 'bzip2', 'bz', 'bzip', 'bzp', 'bzt', 'bz2', 'bz3'])
                            
    
    # TO-DO - consider about on_delete setting here
    entity =  models.ForeignKey(Entity, on_delete=models.CASCADE)
    
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    
    # TO-DO - check if default=now is correct after deployment
    upload_time = models.DateTimeField(default=now)
    
    file = models.FileField(
        _('file'),
        upload_to='files',
        blank=True,
        validators=[file_extension_validator],)
    
    @property
    def artifact_reviews(self):
        return ArtifactReview.objects.filter(artifact=self)
    
    # TO-DO - consider about the logic of this function
    @property
    def feedback(self):
        return Feedback.objects.filter(review_id=ArtifactReview.objects.filter(artifact=self))
    
    @property
    def reviewers(self):
        return [artifact_review.user for artifact_review in self.artifact_reviews]

    
    class Meta:
        db_table = 'artifact'
        verbose_name = _('artifact')
        verbose_name_plural = _('artifact')
    
    

