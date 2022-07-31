from rest_framework import generics, mixins, permissions
from rest_framework.response import Response
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from app.gamification.models.artifact import Artifact
from app.gamification.models.answer import Answer
from app.gamification.models.artifact_review import ArtifactReview
from app.gamification.models.option_choice import OptionChoice
from app.gamification.models.question import Question
from app.gamification.models.question_option import QuestionOption
from app.gamification.models.registration import Registration
from app.gamification.models.survey_section import SurveySection
from app.gamification.models.survey_template import SurveyTemplate
from app.gamification.serializers.survey import OptionChoiceSerializer, QuestionSerializer, SectionSerializer, SurveySerializer
from app.gamification.serializers.answer import AnswerSerializer, ArtifactReviewSerializer


class AnswerList(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    # permission_classes = [IsAdminOrReadOnly]



class AnswerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    # permission_classes = [IsAdminOrReadOnly]

    def get(self, request, answer_pk, *args, **kwargs):
        answer = get_object_or_404(Answer, id=answer_pk)
        serializer = self.get_serializer(answer)
        return Response(serializer.data)

    def put(self, request, answer_pk, *args, **kwargs):
        answer = get_object_or_404(Answer, id=answer_pk)
        answer_text = request.data.get('answer_text')
        answer.answer_text = answer_text
        answer.save()
        serializer = self.get_serializer(answer)
        return Response(serializer.data)

    def delete(self, request, answer_pk, *args, **kwargs):
        answer = get_object_or_404(Answer, id=answer_pk)
        answer.delete()
        return Response(status=204)

class ArtifactAnswer(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    # permission_classes = [IsAdminOrReadOnly]

    def get(self, request, artifact_review_pk, option_pk, *args, **kwargs):
        answer = get_object_or_404(answer, artifact_review_id=artifact_review_pk, option_choice_id = option_pk)
        serializer = self.get_serializer(answer)
        return Response(serializer.data)

    def post(self, request, artifact_review_pk, option_pk, *args, **kwargs):
        option = get_object_or_404(QuestionOption, id=option_pk)
        artifact_review = get_object_or_404(ArtifactReview, id=option_pk)
        answer_text = request.data.get('answer_text')
        answer = Answer.objects.get_or_create(
            question_option=option,
            artifact_review=artifact_review,
            answer_text=answer_text
        )
        serializer = self.get_serializer(answer)
        return Response(serializer.data)

class ArtifactReviewList(generics.ListCreateAPIView):
    queryset = ArtifactReview.objects.all()
    serializer_class = ArtifactReviewSerializer
    # permission_classes = [IsAdminOrReadOnly]

class ArtifactReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ArtifactReview.objects.all()
    serializer_class = ArtifactReviewSerializer
    # permission_classes = [IsAdminOrReadOnly]

    def get(self, request, artifact_review_pk, *args, **kwargs):
        artifact_review = get_object_or_404(ArtifactReview, artifact_review_id=artifact_review_pk)
        serializer = self.get_serializer(artifact_review)
        return Response(serializer.data)

    def delete(self, request, artifact_review_pk, *args, **kwargs):
        artifact_review = get_object_or_404(ArtifactReview, id=artifact_review_pk)
        artifact_review.delete()
        return Response(status=204)

class ArtifactReview(generics.ListCreateAPIView):
    queryset = ArtifactReview.objects.all()
    serializer_class = ArtifactReviewSerializer
    # permission_classes = [IsAdminOrReadOnly]

    def get(self, request, artifact_pk, registration_pk, *args, **kwargs):
        artifact_review = get_object_or_404(ArtifactReview, artifact_id=artifact_pk, user_id = registration_pk)
        serializer = self.get_serializer(artifact_review)
        return Response(serializer.data)

    def post(self, request, artifact_pk, registration_pk, *args, **kwargs):
        artifact = get_object_or_404(Artifact, id=artifact_pk)
        registration = get_object_or_404(Registration, id=registration_pk)
        artifact_review = Answer.objects.get_or_create(
            artifact=artifact,
            user=registration,
        )
        serializer = self.get_serializer(artifact_review)
        return Response(serializer.data)