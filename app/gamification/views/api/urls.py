from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .user import UserList, UserDetail
from .course import CourseList, CourseDetail
from .survey import OptionDetail, OptionList, QuestionDetail, QuestionList, QuestionOptionList, SectionDetail, SectionList, SectionQuestionDetail, SectionQuestionList, SurveyList, SurveyDetail, SurveySectionDetail, SurveySectionList


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'courses': reverse('course-list', request=request, format=format),
        'surveys': reverse('survey-list', request=request, format=format),
        'survey-sections': reverse('survey-section-list', request=request, format=format),
        'sections': reverse('section-list', request=request, format=format),
        'section-questions': reverse('section-question-list', request=request, format=format),
        'questions': reverse('question-list', request=request, format=format),
        'question-options': reverse('question-option-list', request=request, format=format),
        'options': reverse('option-list', request=request, format=format),
    })


urlpatterns = [
    path('', api_root),
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<str:andrew_id>/', UserDetail.as_view(), name='user-detail'),
    path('courses/', CourseList.as_view(), name='course-list'),
    path('courses/<str:id>/', CourseDetail.as_view(), name='course-detail'),

    # RetrieveUpdateDestroyAPIView GET, PUT, PATCH, DELETE
    # ListAPIView GET
    # CreateAPIView GET POST


    # Get the list of all surveys, or Post a new survey
    path('surveys/', SurveyList.as_view(), name='survey-list'),

    # Get detail of a survey, Delete a survey, Update a survey
    path('surveys/<int:survey_pk>/', SurveyDetail.as_view(), name='survey-detail'),

    # Get the sections of a survey, Post a new section of the survey
    path('surveys/<int:survey_pk>/sections/',
         SurveySectionList.as_view(), name='survey-section-list'),

    # Get a section of a survey, Update a section of the survey, Delete a section of the survey
    path('surveys/<int:survey_pk>/sections/<int:section_pk>/',
         SurveySectionDetail.as_view(), name='survey-section-detail'),

    # Get list of sections
    # ListAPIView
    path('sections/', SectionList.as_view(), name='section-list'),

    # Get detail of a section, Update a section, Delete a section
    path('sections/<int:section_pk>/',
         SectionDetail.as_view(), name='section-detail'),

    # Get list of questions of a section, Post a new question of the section
    path('sections/<int:section_pk>/questions/',
         SectionQuestionList.as_view(), name='section-question-list'),

    # Get detail of a question, Update a question, Delete a question
    path('sections/<int:section_pk>/questions/<int:question_pk>/',
         SectionQuestionDetail.as_view(), name='section-question-detail'),

    # Get list of questions
    path('questions/', QuestionList.as_view(), name='question-list'),

    # Get detail of a question, Update a question, Delete a question
    path('questions/<int:question_pk>/',
         QuestionDetail.as_view(), name='question-detail'),

    # Get list of options of a question
    path('questions/<int:question_pk>/options/',
         QuestionOptionList.as_view(), name='question-option-list'),

    # Get list of options, Post a new option
    path('options/', OptionList.as_view(), name='option-list'),

    # Get detail of an option, Update an option, Delete an option
    path('options/<int:option_pk>/', OptionDetail.as_view(), name='option-detail'),

]
