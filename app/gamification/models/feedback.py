from xml.etree.ElementTree import Comment
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

# from .artifact_review import ArtifactReview
# from .user import CustomUser

class Feedback(models.Model):
    
    class PermissionLevel(models.TextChoices):
        Public = 'Public'
        Private = 'Private'

    review_id = models.ForeignKey(ArtifactReview, on_delete=models.CASCADE)
    
    comment = models.TextField(max_length=800, blank=True)
    
    timestamp = models.DateTimeField(default=now)
    
    parent_node = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    
    permission_level = models.TextField(choices=PermissionLevel.choices, default=PermissionLevel.Public)
    
    @property
    def replies(self):
        return Feedback.objects.filter(parent_node=self)
    
    # TO-DO: using 'user' instead of 'registration' might be confusing
    @property
    def user(self):
        return self.review_id.user
    
    def can_view(self, user):
        if self.permission_level == Feedback.PermissionLevel.Public:
            return True
        elif self.permission_level == Feedback.PermissionLevel.Private:
            return self.user == user
        else:
            return False
    class Meta:
        db_table = 'feedback'
        verbose_name = _('feedback')
        verbose_name_plural = _('feedbacks')
