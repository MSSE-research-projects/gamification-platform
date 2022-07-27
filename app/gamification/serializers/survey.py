from rest_framework import serializers

from app.gamification.models import SurveyTemplate, SurveySection
from app.gamification.models.option_choice import OptionChoice
from app.gamification.models.question import Question


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyTemplate
        fields = ['pk', 'name', 'instructions', 'other_info']


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveySection
        fields = ['pk', 'template',
                  'title', 'description', 'is_required']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['pk', 'section', 'text', 'is_required', 'is_multiple',
                  'dependent_question', 'question_type', 'option_choices']


class OptionChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionChoice
        fields = ['pk', 'text']


class SurveySectionSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True)

    class Meta:
        model = SurveyTemplate
        fields = ['pk', 'name', 'instructions', 'other_info', 'sections']


class SectionQuestionsSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = SurveySection
        fields = ['pk', 'template', 'title', 'description',
                  'is_required', 'questions']


class QuestionOptionsSerializer(serializers.ModelSerializer):
    options = OptionChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ['pk', 'section', 'text', 'is_required', 'is_multiple',
                  'dependent_question', 'question_type', 'option_choices', 'options']