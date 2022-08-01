from rest_framework import serializers

from app.gamification.models import Answer, ArtifactReview, ArtifactFeedback
from app.gamification.models.option_choice import OptionChoice
from app.gamification.models.question import Question


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['pk', 'question_option', 'artifact_review', 'answer_text']


class ArtifactFeedbackSerializer(serializers.ModelSerializer):
    model = ArtifactFeedback
    fields = ['pk', 'question_option',
              'artifact_review', 'answer_text', 'page']


class ArtifactReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtifactReview
        fields = ['pk', 'artifact', 'user']
