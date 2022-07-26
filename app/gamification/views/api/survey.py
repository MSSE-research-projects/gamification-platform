from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response

from app.gamification.models import CustomUser
from app.gamification.models.option_choice import OptionChoice
from app.gamification.models.question import Question
from app.gamification.models.question_option import QuestionOption
from app.gamification.models.survey_section import SurveySection
from app.gamification.models.survey_template import SurveyTemplate
from app.gamification.serializers import UserSerializer
from app.gamification.serializers.survey import OptionChoiceSerializer, QuestionOptionsSerializer, QuestionSerializer, SectionQuestionsSerializer, SectionSerializer, SurveySectionSerializer, SurveySerializer


class SurveyList(generics.ListCreateAPIView):
    queryset = SurveyTemplate.objects.all()
    serializer_class = SurveySerializer


class SurveyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SurveyTemplate.objects.all()
    serializer_class = SurveySerializer

    def get(self, request, survey_pk, *args, **kwargs):
        survey = SurveyTemplate.objects.get(id=survey_pk)
        serializer = self.get_serializer(survey)
        return Response(serializer.data)

    def put(self, request, survey_pk, *args, **kwargs):
        survey = SurveyTemplate.objects.get(id=survey_pk)
        name = request.data.get('name')
        instructions = request.data.get('instructions')
        other_info = request.data.get('other_info')
        survey.name = name
        survey.instructions = instructions
        survey.other_info = other_info
        survey.save()
        serializer = self.get_serializer(survey)
        return Response(serializer.data)

    def delete(self, request, survey_pk, *args, **kwargs):
        sections = SurveyTemplate.objects.get(id=survey_pk)
        sections.delete()
        return Response(status=204)


class SurveySectionList(generics.ListCreateAPIView):
    queryset = SurveyTemplate.objects.all()
    serializer_class = SectionSerializer

    def get(self, request, survey_pk, *args, **kwargs):
        sections = SurveySection.objects.filter(template=survey_pk)
        serializer = self.get_serializer(sections, many=True)
        return Response(serializer.data)

    def post(self, request, survey_pk, *args, **kwargs):
        title = request.data.get('title')
        description = request.data.get('description')
        is_required = True if request.data.get(
            'is_required') == 'true' else False
        section = SurveySection(template_id=survey_pk, title=title,
                                description=description, is_required=is_required)
        section.save()
        serializer = self.get_serializer(section)
        return Response(serializer.data)


class SurveySectionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SurveyTemplate.objects.all()
    serializer_class = SectionSerializer

    def get(self, request, survey_pk, section_pk, *args, **kwargs):
        section = SurveySection.objects.get(id=section_pk, template=survey_pk)
        serializer = self.get_serializer(section)
        return Response(serializer.data)

    def put(self, request, survey_pk, section_pk, *args, **kwargs):
        section = SurveySection.objects.get(id=section_pk, template=survey_pk)
        title = request.data.get('title')
        description = request.data.get('description')
        is_required = True if request.data.get(
            'is_required') == 'true' else False
        section.title = title
        section.description = description
        section.is_required = is_required
        section.save()
        serializer = self.get_serializer(section)
        return Response(serializer.data)

    def delete(self, request, survey_pk, section_pk, *args, **kwargs):
        section = SurveySection.objects.get(id=section_pk, template=survey_pk)
        section.delete()
        return Response(status=204)


class SectionList(generics.ListAPIView):
    queryset = SurveySection.objects.all()
    serializer_class = SectionSerializer


class SectionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SurveySection.objects.all()
    serializer_class = SectionSerializer

    def get(self, request, section_pk, *args, **kwargs):
        sections = SurveySection.objects.get(id=section_pk)
        serializer = self.get_serializer(sections)
        return Response(serializer.data)

    def put(self, request, section_pk, *args, **kwargs):
        section = SurveySection.objects.get(id=section_pk)
        title = request.data.get('title')
        description = request.data.get('description')
        is_required = True if request.data.get(
            'is_required') == 'true' else False
        section.title = title
        section.description = description
        section.is_required = is_required
        section.save()
        serializer = self.get_serializer(section)
        return Response(serializer.data)

    def delete(self, request, section_pk, *args, **kwargs):
        section = SurveySection.objects.get(id=section_pk)
        section.delete()
        return Response(status=204)


class SectionQuestionList(generics.ListCreateAPIView):
    queryset = SurveySection.objects.all()
    serializer_class = QuestionSerializer

    def get(self, request, section_pk, *args, **kwargs):
        questions = Question.objects.filter(section=section_pk)
        serializer = self.get_serializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request, section_pk, *args, **kwargs):
        text = request.data.get('text')
        is_required = True if request.data.get(
            'is_required') == 'true' else False
        is_multiple = True if request.data.get(
            'is_multiple') == 'true' else False
        dependent_question = request.data.get('dependent_question') if request.data.get(
            'dependent_question') != '' else None
        question_type = request.data.get('question_type')
        section = SurveySection.objects.get(id=section_pk)
        question = Question(
            text=text, is_required=is_required, is_multiple=is_multiple, dependent_question=dependent_question, question_type=question_type, section=section)
        question.save()
        serializer = self.get_serializer(question)
        return Response(serializer.data)


class SectionQuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SurveySection.objects.all()
    serializer_class = QuestionSerializer

    def get(self, request, section_pk, question_pk, *args, **kwargs):
        question = Question.objects.get(id=question_pk, section=section_pk)
        serializer = self.get_serializer(question)
        return Response(serializer.data)

    def put(self, request, section_pk, question_pk, *args, **kwargs):
        question = Question.objects.get(id=question_pk, section=section_pk)
        text = request.data.get('text')
        is_required = True if request.data.get(
            'is_required') == 'true' else False
        is_multiple = True if request.data.get(
            'is_multiple') == 'true' else False
        dependent_question = request.data.get('dependent_question') if request.data.get(
            'dependent_question') != '' else None
        question_type = request.data.get('question_type')
        question.text = text
        question.is_required = is_required
        question.is_multiple = is_multiple
        question.dependent_question = dependent_question
        question.question_type = question_type
        question.save()
        serializer = self.get_serializer(question)
        return Response(serializer.data)

    def delete(self, request, section_pk, question_pk, *args, **kwargs):
        question = Question.objects.get(id=question_pk, section=section_pk)
        question.delete()
        return Response(status=204)


class QuestionList(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get(self, request, question_pk, *args, **kwargs):
        question = Question.objects.get(id=question_pk)
        serializer = self.get_serializer(question)
        return Response(serializer.data)

    def put(self, request, question_pk, *args, **kwargs):
        question = Question.objects.get(id=question_pk)
        text = request.data.get('text')
        print(request.data.get('is_required'))
        is_required = True if request.data.get(
            'is_required') == 'true' else False
        is_multiple = True if request.data.get(
            'is_multiple') == 'true' else False
        dependent_question = request.data.get('dependent_question') if request.data.get(
            'dependent_question') != '' else None
        question_type = request.data.get('question_type')
        question.text = text
        question.is_required = is_required
        question.is_multiple = is_multiple
        question.dependent_question = dependent_question
        question.question_type = question_type
        question.save()
        serializer = self.get_serializer(question)
        return Response(serializer.data)

    def delete(self, request, question_pk, *args, **kwargs):
        question = Question.objects.get(id=question_pk)
        question.delete()
        return Response(status=204)


class QuestionOptionList(generics.CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = OptionChoiceSerializer

    def get(self, request, question_pk, *args, **kwargs):
        question = Question.objects.get(id=question_pk)
        options = question.options
        serializer = self.get_serializer(options, many=True)
        return Response(serializer.data)


class OptionList(generics.CreateAPIView):
    queryset = OptionChoice.objects.all()
    serializer_class = OptionChoiceSerializer

    def get(self, request, *args, **kwargs):
        options = OptionChoice.objects.all()
        serializer = self.get_serializer(options, many=True)
        return Response(serializer.data)


class OptionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = OptionChoice.objects.all()
    serializer_class = OptionChoiceSerializer

    def get(self, request, option_pk, *args, **kwargs):
        option = OptionChoice.objects.get(id=option_pk)
        serializer = self.get_serializer(option)
        return Response(serializer.data)

    def put(self, request, option_pk, *args, **kwargs):
        option = OptionChoice.objects.get(id=option_pk)
        text = request.data.get('text')
        option.text = text
        option.save()
        serializer = self.get_serializer(option)
        return Response(serializer.data)
