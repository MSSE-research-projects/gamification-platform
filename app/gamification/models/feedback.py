from xml.etree.ElementTree import Comment
from MySQLdb import Timestamp
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from .artifact_review import ArtifactReview
from .user import CustomUser

class Feedback(models.Model):
    
    class PermissionLevel(models.TextChoices):
        Public = 'Public'
        Private = 'Private'

    review_id = models.ForeignKey(ArtifactReview, on_delete=models.CASCADE)
    
    comment = models.TextField(blank=True)
    
    timestamp = models.DateTimeField(default=now)
    
    parent_node = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    
    permission_level = models.TextField(choices=PermissionLevel.choices, default=PermissionLevel.Public)
    
    # TO-DO - is user a foreign key?
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    def replies(self):
        return Feedback.objects.filter(parent_node=self)

    class Meta:
        db_table = 'feedback'
        verbose_name = _('feedback')
        verbose_name_plural = _('feedbacks')
