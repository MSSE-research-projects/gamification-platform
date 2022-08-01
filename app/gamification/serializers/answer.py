from rest_framework import serializers

from app.gamification.models import Answer, ArtifactReview, ArtifactFeedback
from app.gamification.models.option_choice import OptionChoice
from app.gamification.models.question import Question



class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['pk', 'artifact', 'questionOption', 'answerText']

class ArtifactFeedbackSerializer(serializers.ModelSerializer):
    answer = AnswerSerializer()
    class Meta:
        model = ArtifactFeedback
        fields = ['pk', 'page', 'answer']


class ArtifactReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtifactReview
        fields = ['pk', 'artifact', 'regisration']

