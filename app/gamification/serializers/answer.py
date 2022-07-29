from rest_framework import serializers

from app.gamification.models import SurveyTemplate, SurveySection, Answer, ArtifactReview
from app.gamification.models.option_choice import OptionChoice
from app.gamification.models.question import Question


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['pk', 'artifact', 'questionOption', 'answerText']


class ArtifactReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtifactReview
        fields = ['pk', 'artifact', 'user']