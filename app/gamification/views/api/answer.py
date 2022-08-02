import json
from rest_framework import generics, mixins, permissions
from rest_framework.response import Response
from django.contrib import messages
from django.shortcuts import get_object_or_404
from app.gamification.models.option_choice import OptionChoice
from app.gamification.models.artifact import Artifact
from app.gamification.models.answer import Answer, ArtifactFeedback
from app.gamification.models.artifact_review import ArtifactReview
from app.gamification.models.question import Question
from app.gamification.models.question_option import QuestionOption
from app.gamification.models.registration import Registration
from app.gamification.serializers.answer import AnswerSerializer, ArtifactReviewSerializer, ArtifactFeedbackSerializer, CreateAnswerSerializer


class AnswerList(generics.ListAPIView):
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
        return Response(serializer.errors, status=400)

    def delete(self, request, answer_pk, *args, **kwargs):
        answer = get_object_or_404(Answer, id=answer_pk)
        answer.delete()
        return Response(status=204)


class FeedbackDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ArtifactFeedback.objects.all()
    serializer_class = ArtifactFeedbackSerializer
    # permission_classes = [IsAdminOrReadOnly]

    def get(self, request, feedback_pk, *args, **kwargs):
        feedback = get_object_or_404(ArtifactFeedback, id=feedback_pk)
        serializer = self.get_serializer(feedback)
        return Response(serializer.data)

    def put(self, request, feedback_pk, *args, **kwargs):
        feedback = get_object_or_404(ArtifactFeedback, id=feedback_pk)
        answer_text = request.data.get('answer_text')
        feedback.answer_text = answer_text
        feedback.save()
        serializer = self.get_serializer(feedback)
        return Response(serializer.errors, status=400)

    def delete(self, request, feedback_pk, *args, **kwargs):
        feedback = get_object_or_404(ArtifactFeedback, id=feedback_pk)
        feedback.delete()
        return Response(status=204)


class ArtifactAnswerList(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    # permission_classes = [IsAdminOrReadOnly]

    def get(self, request, artifact_review_pk, *args, **kwargs):
        answer = Answer.objects.filter(artifact_review_id=artifact_review_pk)
        serializer = self.get_serializer(answer)
        return Response(serializer.data)


class CreateArtifactAnswer(generics.UpdateAPIView):
    queryset = Answer.objects.all()
    serializer_class = CreateAnswerSerializer
    # permission_classes = [IsAdminOrReadOnly]

    def put(self, request, artifact_review_pk, question_pk, *args, **kwargs):
        # Multiple Choice text -> option_text
        artifact_review = get_object_or_404(
            ArtifactReview, id=artifact_review_pk)
        # Text input -> answer_text []
        self.answer_texts = json.loads(request.data.get('answer_text'))
        # get_object_or_404
        question = Question.objects.get(id=question_pk)
        question_type = question.question_type
        page = request.data.get('page')
        if question_type == Question.Question_type.MULTIPLECHOICE:
            # delete original answer
            question_options = question.options
            # question_options = ['a', 'b', 'c', 'd']
            counter = len(self.answer_texts)
            for question_option in question_options:
                if counter == 0:
                    break
                if Answer.objects.filter(question_option=question_option, artifact_review=artifact_review).count() > 0:
                    answer = Answer.objects.get(
                        question_option=question_option, artifact_review=artifact_review)
                    # answer {answer_text= 'b', question_option= question_option(optionChoice=b, question=question), artifact_review= aritfact_review}
                    # check answer_texts whether empty
                    # answer_text = ['a']
                    if len(self.answer_texts) > 0:
                        current_answer = self.answer_texts.pop(0)
                        counter -= 1
                        answer.answer_text = current_answer
                        question_option = QuestionOption.objects.get(
                            option_choice=OptionChoice.objects.get(text=current_answer))
                        answer.question_option = question_option
                        answer.save()
                    else:
                        print('delete')
                        # original answers more than new answers
                        answer.delete()
            # new answers more than original answers
            while len(self.answer_texts) != 0:
                current_answer = self.answer_texts.pop(0)
                question_option = QuestionOption.objects.get(
                    option_choice=OptionChoice.objects.get(text=current_answer))
                answer = Answer(answer_text=current_answer,
                                question_option=question_option, artifact_review=artifact_review)
                answer.save()
            serializer = self.get_serializer(answer)
            return Response(serializer.data)

        elif question_type == Question.Question_type.FIXEDTEXT or question_type == Question.Question_type.MULTIPLETEXT:
            question_option = question.options[0]
            answers = Answer.objects.filter(
                question_option=question_option, artifact_review=artifact_review)
            for answer in answers:
                if len(self.answer_texts) > 0:
                    current_answer = self.answer_texts.pop(0)
                    answer.answer_text = current_answer
                    answer.save()
                else:
                    # original answers more than new answers
                    answer.delete()
            while len(self.answer_texts) != 0:
                current_answer = self.answer_texts.pop(0)
                answer = Answer(answer_text=current_answer,
                                question_option=question_option, artifact_review=artifact_review)
                answer.save()
            serializer = self.get_serializer(answer)
            return Response(serializer.data)
        else:
            self.serializer_class = ArtifactFeedbackSerializer
            answer, _ = ArtifactFeedback.objects.get_or_create(
                question_option=question_option,
                artifact_review=artifact_review,
                # TODO: Need to fix
                answer_text=self.answer_texts[0],
                page=page,
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

    def get(self, request, artifact_review_id, *args, **kwargs):
        artifact_review = get_object_or_404(
            ArtifactReview, artifact_review_pk=artifact_review_id)
        serializer = self.get_serializer(artifact_review)
        return Response(serializer.data)

    def delete(self, request, artifact_review_id, *args, **kwargs):
        artifact_review = get_object_or_404(
            ArtifactReview, id=artifact_review_id)
        artifact_review.delete()
        return Response(status=204)


class CreateArtifactReview(generics.ListCreateAPIView):
    queryset = ArtifactReview.objects.all()
    serializer_class = ArtifactReviewSerializer
    # permission_classes = [IsAdminOrReadOnly]

    def get(self, request, artifact_pk, registration_pk, *args, **kwargs):
        artifact_review = get_object_or_404(
            ArtifactReview, artifact_id=artifact_pk, user_id=registration_pk)
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
