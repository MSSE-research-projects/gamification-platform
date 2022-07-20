from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from app.gamification.decorators import user_role_check
from app.gamification.models import Assignment, Registration, SurveySection, FeedbackSurvey, Question, QuestionOption
from app.gamification.models.option_choice import OptionChoice
from app.gamification.models.survey_template import SurveyTemplate

from .section_question import SECTION_QUESTION


@login_required
@user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA])
def add_survey(request, course_id, assignment_id):
    if request.method == 'POST':
        survey_template_name = request.POST.get('template_name')
        survey_template_instruction = request.POST.get('instructions')
        survey_template_other_info = request.POST.get('other_info')
        feedback_survey_date_released = request.POST.get('date_released')
        feedback_survey_date_due = request.POST.get('date_due')

        survey_template = SurveyTemplate(
            name=survey_template_name, instructions=survey_template_instruction, other_info=survey_template_other_info)
        survey_template.save()
        feedback_survey = FeedbackSurvey(
            assignment_id=assignment_id,
            template=survey_template,
            date_released=feedback_survey_date_released,
            date_due=feedback_survey_date_due
        )
        feedback_survey.save()
        messages.success(request, 'Survey added successfully')
        return redirect('survey_list', course_id, assignment_id)
    else:
        return render(request, 'add_survey.html', {'course_id': course_id, 'assignment_id': assignment_id})


@login_required
@user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA])
def survey_list(request, course_id, assignment_id):
    if request.method == 'GET':
        assignment = Assignment.objects.get(id=assignment_id)

        template = assignment.survey_template
        if(template is None):
            messages.error(
                request, 'No survey template found for this assignment')
            # TODO: redirect page?
            return redirect('survey_list', course_id, assignment_id)

        survey = dict()
        survey['instance'] = template

        sections = list()
        for section in survey['instance'].sections:
            section_dict = dict()
            section_dict['instance'] = section
            questions = list()
            for question in section_dict['instance'].questions:
                question_dict = dict()
                question_dict['instance'] = question
                question_options = list()
                for option in question_dict['instance'].options:
                    question_option_dict = dict()
                    question_option_dict['instance'] = option
                    question_options.append(question_option_dict)
                question_dict['options'] = question_options
                questions.append(question_dict)
            section_dict['questions'] = questions
            sections.append(section_dict)
        survey['sections'] = sections

        return render(request, 'survey_detail.html', {'course_id': course_id, 'assignment_id': assignment_id,
                                                      'survey': survey, 'section_question': SECTION_QUESTION})
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
            sections = SurveySection.objects.filter(title=section_title)
            if len(sections) == 0:
                survey_section = SurveySection(
                    title=section_title, is_required=is_required, template=survey_template)
                survey_section.save()
            else:
                message_info = 'Cannot add duplicate section.'
                messages.info(request, message_info)
        return redirect('survey_list', course_id, assignment_id)
    else:
        return render(request, 'survey_detail.html', {'course_id': course_id, 'assignment_id': assignment_id})


@login_required
@user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA])
def add_question(request, course_id, assignment_id, section_id):
    if request.method == 'POST':
        text = request.POST.get('text')
        section = SurveySection.objects.get(id=section_id)
        optional = request.POST.get('is_required')
        is_required = False if optional == 'on' else True
        question_type = Question.Question_type.MULTIPLECHOICE if request.POST.get(
            'multiple_choice') == 'on' else Question.Question_type.MULTIPLETEXT if request.POST.get('multiple_text') == 'on' else Question.Question_type.FIXEDTEXT
        print(question_type)
        # question_type = [fixed_text, multiple_choice, multiple_text]
        # option = 'on'
        # fixed_tex
        #      - number_of_text: int
        #
        # multiple_choice:
        #      - option_choice_text: string ???
        # multiple_text:
        #      - number_of_text: int
        questions = Question.objects.filter(text=text, section=section)
        if len(questions) == 0:
            question = Question(text=text, section=section,
                                is_required=is_required, question_type=question_type)
            question.save()
        else:
            message_info = 'Cannot add duplicate question.'
            messages.info(request, message_info)
        if question_type == 'multiple_choice':
            option_choice_text = request.POST.getlist('option_text')
            option_choice = OptionChoice(text=option_choice_text)
            option_choice.save()
            question_option = QuestionOption(
                option_choice=option_choice, question=question, number_of_text=1)
            question_option.save()
        else:
            option_choice_text = ''
            number_of_text = request.POST.get('number_of_text')
            option_choice = OptionChoice(text=option_choice_text)
            option_choice.save()
            question_option = QuestionOption(
                option_choice=option_choice, question=question, number_of_text=number_of_text)
            question_option.save()
        return redirect('survey_list', course_id, assignment_id)
    else:
        return render(request, 'survey_detail.html', {'course_id': course_id, 'assignment_id': assignment_id, 'section_id': section_id})


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
