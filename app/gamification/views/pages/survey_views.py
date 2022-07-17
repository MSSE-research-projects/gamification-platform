from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse


from app.gamification.decorators import admin_required, user_role_check
from app.gamification.forms import AddSurveyForm
from app.gamification.models import Assignment, Course, CustomUser, Registration, Team, Membership, SurveySection, SurveyTemplate, FeedbackSurvey, Question

from .section_question import SECTION_QUESTION


@login_required
@user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA])
def add_survey(request, course_id, assignment_id):
    if request.method == 'GET':
        form = AddSurveyForm(request.GET, label_suffix='')
        return render(request, 'survey.html', {'course_id': course_id, 'assignment_id': assignment_id, 'form': form})
    elif request.method == 'POST':
        form = AddSurveyForm(request.POST, label_suffix='')
        if form.is_valid():
            form.save()
        return render(request, 'section.html', {'course_id': course_id, 'assignment_id': assignment_id, 'form': form})
    else:
        return render(request, 'section.html', {'course_id': course_id, 'assignment_id': assignment_id})


@login_required
@user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA])
def survey_list(request, course_id, assignment_id):
    if request.method == 'GET':
        feedback_survey = FeedbackSurvey.objects.get(
            assignment__pk=assignment_id)
        survey_template = feedback_survey.survey_template
        survey_sections = SurveySection.objects.filter(
            survey_template=survey_template)
        survey = {}
        for survey_section in survey_sections:
            survey_questions = Question.objects.filter(
                survey_section=survey_section)
            survey[survey_section] = list(survey_questions)
        return render(request, 'survey_list.html', {'course_id': course_id, 'assignment_id': assignment_id, 'survey': survey, 'section_question': SECTION_QUESTION})
    else:
        return redirect('survey_list', course_id, assignment_id)


@login_required
@user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA])
def add_section(request, course_id, assignment_id):
    def get_all_sections(self, assignment_id):
        # feedback_surveys = FeedbackSurvey.objects.filter(assignment=assignment_id, template=)
        # sections = Section.objects.filter(assignment=assignment_id)
        # return SurveySection.objects.all()
        pass

    if request.method == 'GET':
        sections = get_all_sections(request, assignment_id)
        section_title_list = list(SECTION_QUESTION.keys())
        context = {
            'sections': sections,
            'section_title_list': section_title_list,
            'course_id': course_id,
            'assignment_id': assignment_id,
        }
        return render(request, 'section.html', context)
    elif request.method == 'POST':
        return render(request, 'question.html', {'course_id': course_id, 'assignment_id': assignment_id})
    else:
        return render(request, 'question.html', {'course_id': course_id, 'assignment_id': assignment_id})


@login_required
@user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA])
def add_question(request, course_id, assignment_id):
    return render(request, 'feedback.html')


@login_required
@user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA])
def delete_section(request, course_id, assignment_id, section_id):
    return render(request, 'feedback.html')


@login_required
@user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA])
def edit_section(request, course_id, assignment_id, section_id):
    return render(request, 'feedback.html')


@login_required
@user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA])
def edit_question(request, course_id, assignment_id, section_id, question_id):
    return render(request, 'feedback.html')


@login_required
@user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA])
def delete_question(request, course_id, assignment_id, section_id, question_id):
    return render(request, 'feedback.html')
