from re import template
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render


from app.gamification.decorators import admin_required, user_role_check
from app.gamification.forms import AddSurveyForm
from app.gamification.models import Assignment, Registration, SurveySection, FeedbackSurvey, Question, option_group, survey_template

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
            template = form.save()
        assignment = Assignment.objects.get(id=assignment_id)
        feedback_survey = FeedbackSurvey(
            assignment=assignment, template=template)
        feedback_survey.save()
        return redirect('survey_list', course_id, assignment_id)
    else:
        return render(request, 'survey_detail.html', {'course_id': course_id, 'assignment_id': assignment_id})


@login_required
@user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA])
def survey_list(request, course_id, assignment_id):
    if request.method == 'GET':
        assignment = Assignment.objects.get(id=assignment_id)
        feedback_survey = FeedbackSurvey.objects.filter(
            assignment=assignment)
        if(len(feedback_survey) >= 1):
            feedback_survey = feedback_survey[0]
            survey_template = feedback_survey.template
            survey_sections = SurveySection.objects.filter(
                template=survey_template)
        else:
            survey_sections = []
        survey = {}
        for survey_section in survey_sections:
            survey_questions = Question.objects.filter(
                section=survey_section)
            survey[survey_section] = list(survey_questions)
        return render(request, 'survey_detail.html', {'course_id': course_id, 'assignment_id': assignment_id, 'survey': survey, 'section_question': SECTION_QUESTION})
    else:
        return redirect('survey_list', course_id, assignment_id)


@login_required
@user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA])
def add_section(request, course_id, assignment_id):
    if request.method == 'POST':
        section_title = request.POST.get('section_title')
        optional = request.POST.get('optional')
        is_required = False if optional == 'on' else True
        assignment = Assignment.objects.get(id=assignment_id)
        feedback_survey = FeedbackSurvey.objects.filter(
            assignment=assignment)
        # TODO FIX LENGTH
        if(len(feedback_survey) >= 1):
            feedback_survey = feedback_survey[0]
            survey_template = feedback_survey.template
            survey_section = SurveySection(
                title=section_title, is_required=is_required, template=survey_template)
            survey_section.save()
        return redirect('survey_list', course_id, assignment_id)
    else:
        return render(request, 'survey_detail.html', {'course_id': course_id, 'assignment_id': assignment_id})


@login_required
@user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA])
def add_question(request, course_id, assignment_id, section_id):
    if request.method == 'POST':
        text = request.POST.get('text')
        section = SurveySection.objects.get(id=section_id)
        # is_required = request.POST.get('is_required')
        # question_type = request.POST.get('question_type')
        question = Question(text=text,
                            section=section,
                            # is_required=is_required,
                            question_type=Question.Question_type.MULTIPLECHOICE)

        question.save()
        return redirect('survey_list', course_id, assignment_id)
    else:
        return render(request, 'survey_detail.html', {'course_id': course_id, 'assignment_id': assignment_id})


@ login_required
@ user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA])
def delete_section(request, course_id, assignment_id, section_id):
    if request.method == 'GET':
        survey_section = get_object_or_404(SurveySection, id=section_id)
        question = Question.objects.filter(section=survey_section)
        question.delete()
        survey_section.delete()
        return redirect('survey_list', course_id, assignment_id)
    else:
        return redirect('survey_list', course_id, assignment_id)


@ login_required
@ user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA])
def edit_section(request, course_id, assignment_id, section_id):
    if request.method == 'POST':
        assignment = get_object_or_404(Question, id=assignment_id)
        survey_template = assignment.survey_template
        survey_section = get_object_or_404(
            SurveySection, id=section_id, template=survey_template)
        section_title = request.POST.get('section_title')
        optional = request.POST.get('optional')
        is_required = False if optional == 'on' else True
        survey_section.title = section_title
        survey_section.is_required = is_required
        survey_section.save()
    return redirect('survey_list', course_id, assignment_id)


@login_required
@user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA])
def edit_question(request, course_id, assignment_id, section_id, question_id):
    if request.method == 'POST':
        assignment = get_object_or_404(Question, id=assignment_id)
        survey_template = assignment.survey_template
        survey_section = get_object_or_404(
            SurveySection, id=section_id, template=survey_template)
        question = get_object_or_404(
            Question, id=question_id, section=survey_section)
        text = request.POST.get('text')
        is_required = request.POST.get('is_required')
        question_type = request.POST.get('question_type')
        question.text = text
        question.is_required = is_required
        question.question_type = question_type
        question.save()
    return redirect('survey_list', course_id, assignment_id)


@login_required
@user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA])
def delete_question(request, course_id, assignment_id, section_id, question_id):
    if request.method == 'GET':
        question = get_object_or_404(
            Question, id=question_id, section=section_id)
        question.delete()
        return redirect('survey_list', course_id, assignment_id)
    else:
        return redirect('survey_list', course_id, assignment_id)
