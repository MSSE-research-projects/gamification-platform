import os
import pytz
from pytz import timezone
from datetime import datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.http import FileResponse
from django.utils.timezone import now
from app.gamification.utils import parse_datetime
from app.gamification.decorators import admin_required, user_role_check
from app.gamification.forms import AssignmentForm, SignUpForm, ProfileForm, CourseForm, PasswordResetForm, ArtifactForm, TodoListForm
from app.gamification.models import Assignment, Course, CustomUser, Registration, Team, Membership, Artifact, Individual, FeedbackSurvey, Question, OptionChoice, QuestionOption
from app.gamification.models.artifact_review import ArtifactReview
from app.gamification.models.survey_section import SurveySection
from app.gamification.models.survey_template import SurveyTemplate
from app.gamification.models.todo_list import TodoList

LA = timezone('America/Los_Angeles')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, label_suffix='')
        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('profile')
    else:
        form = SignUpForm(label_suffix='')

    return render(request, 'signup.html', {'form': form})


def signin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to where they were asked to login
                return redirect('profile')
    else:
        form = AuthenticationForm()

    return render(request=request, template_name="signin.html", context={"form": form})


class PasswordResetView(auth_views.PasswordResetView):
    form_class = PasswordResetForm
    template_name = 'password_reset.html'


def signout(request):
    logout(request)
    return redirect('signin')


@admin_required
def email_user(request, andrew_id):
    current_site = get_current_site(request)
    if request.method == 'POST':
        user = get_object_or_404(CustomUser, andrew_id=andrew_id)

        subject = 'Gamification: Activate your account'
        message = 'Please click the link below to reset your password, '\
            'and then login into the system to activate your account:\n\n'
        message += f'http://{current_site.domain}{reverse("password_reset")}\n\n'
        message += 'Your Andrew ID: ' + user.andrew_id + '\n\n'
        message += 'If you did not request this, please ignore this email.\n'

        user.email_user(subject, message)

        redirect_path = request.POST.get('next', reverse('dashboard'))
        messages.info(request, f'An email has been sent to {user.andrew_id}.')
    elif request.method == 'GET':
        redirect_path = request.GET.get('next', reverse('dashboard'))
    else:
        redirect_path = reverse('dashboard')

    return redirect(redirect_path)


@login_required
def dashboard(request):
    def get_registrations(user):
        registration = []
        for reg in Registration.objects.filter(users=user):
            if reg.userRole == Registration.UserRole.Student and reg.courses.visible == False:
                continue
            else:
                registration.append(reg)
        return registration

    def get_todo_list(user):
        return TodoList.objects.filter(user=user)

    if request.method == 'GET':
        andrew_id = request.user.andrew_id
        form = TodoListForm(label_suffix='')
        unsorted_registration = get_registrations(request.user)
        # TODO: sort registration by semester in a better way
        registration = sorted(unsorted_registration,
                              key=lambda x: x.courses.semester, reverse=True)
        todo_list = get_todo_list(request.user)
        # sort todo list by due date, excluding NoneType
        sorted_todo_list = sorted(
            todo_list, key=lambda x: x.due_date if x.due_date else now(), reverse=False)
        # TODO: change timezone
        time_now = now()
        user = request.user
        context = {'registration': registration, 'request_user': user, 'form': form,
                   'andrew_id': andrew_id, 'todo_list': sorted_todo_list, 'time_now': time_now}
        return render(request, 'dashboard.html', context)


@login_required
def add_todo_list(request):
    if request.method == 'POST':
        form = TodoListForm(request.POST, label_suffix='')
        if form.is_valid():
            # todo_list = form.save(commit=False)
            # todo_list.user = request.user
            form.save()
        else:
            print("form is not valid")
        return redirect('dashboard')


@login_required
def delete_todo_list(request, todo_list_id):
    if request.method == 'GET':
        todo_list = get_object_or_404(TodoList, pk=todo_list_id)
        # check if the user is the owner of the todo list
        user = request.user
        # if todo_list.user == user:
        #     todo_list.delete()
        #     return redirect('dashboard')
        todo_list.delete()
        return redirect('dashboard')
    else:
        print("not deleted")
        return redirect('dashboard')


@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES,
                           instance=user, label_suffix='')

        if form.is_valid():
            user = form.save()
            form = ProfileForm(instance=user)
        else:
            user = CustomUser.objects.get(andrew_id=user.andrew_id)

    else:
        form = ProfileForm(instance=user)

    return render(request, 'profile.html', {'user': user, 'form': form})


@login_required
@admin_required(redirect_field_name=None, login_url='dashboard')
def instructor_admin(request):
    return render(request, 'instructor_admin.html')


@login_required
@user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA])
def add_survey(request, course_id, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)

    if request.method == 'POST':
        survey_template_name = request.POST.get('template_name').strip()
        survey_template_instruction = request.POST.get('instructions')
        survey_template_other_info = request.POST.get('other_info')
        feedback_survey_date_released = parse_datetime(
            request.POST.get('date_released'))
        feedback_survey_date_due = parse_datetime(request.POST.get('date_due'))
        survey_template = SurveyTemplate(
            name=survey_template_name, instructions=survey_template_instruction, other_info=survey_template_other_info)
        survey_template.save()
        feedback_survey = FeedbackSurvey(
            assignment=assignment,
            template=survey_template,
            date_released=feedback_survey_date_released,
            date_due=feedback_survey_date_due
        )
        feedback_survey.save()

        if survey_template_name == "Default Template":

            default_survey_template = get_object_or_404(
                SurveyTemplate, is_template=True, name="Survey Template")
            for default_section in default_survey_template.sections:
                section = SurveySection(template=survey_template,
                                        title=default_section.title,
                                        description=default_section.description,
                                        is_required=default_section.is_required,
                                        )
                section.save()
                for default_question in default_section.questions:
                    question = Question(section=section,
                                        text=default_question.text,
                                        question_type=default_question.question_type,
                                        dependent_question=default_question.dependent_question,
                                        is_required=default_question.is_required,
                                        is_multiple=default_question.is_multiple,
                                        )
                    question.save()
                    for default_option in default_question.options:
                        question_option = QuestionOption(
                            question=question,
                            option_choice=default_option.option_choice,
                            number_of_text=default_option.number_of_text,
                        )
                        question_option.save()

        else:

            # Automatically create a section and question for artifact
            artifact_section = SurveySection.objects.create(
                template=survey_template,
                title='Artifact',
                description='Please review the artifact.',
                is_required=False,
            )
            artifact_question = Question.objects.create(
                section=artifact_section,
                text='',
                question_type=Question.QuestionType.SLIDEREVIEW,
            )
            empty_option, _ = OptionChoice.objects.get_or_create(text='')
            QuestionOption.objects.create(
                question=artifact_question, option_choice=empty_option)

        return redirect('edit_survey', course_id, assignment_id)
    else:
        feedback_survey = FeedbackSurvey.objects.filter(assignment=assignment)
        if feedback_survey.count() > 0:
            return redirect('edit_survey', course_id, assignment_id)
        return render(request, 'add_survey.html', {'course_id': course_id, 'assignment_id': assignment_id})


@login_required
@user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA])
def edit_survey_template(request, course_id, assignment_id):
    if request.method == 'POST':

        survey_template_name = request.POST.get('template_name')
        survey_template_instruction = request.POST.get('instructions')
        survey_template_other_info = request.POST.get('other_info')
        feedback_survey_date_released = parse_datetime(
            request.POST.get('date_released'))
        feedback_survey_date_due = parse_datetime(request.POST.get('date_due'))
        feedback_survey = FeedbackSurvey.objects.get(
            assignment_id=assignment_id
        )
        survey_template = feedback_survey.template

        survey_template.name = survey_template_name
        survey_template.instructions = survey_template_instruction
        survey_template.other_info = survey_template_other_info
        survey_template.save()

        feedback_survey.template = survey_template
        feedback_survey.date_released = feedback_survey_date_released
        feedback_survey.date_due = feedback_survey_date_due
        feedback_survey.save()
        return redirect('edit_survey', course_id, assignment_id)
    else:
        assignment = get_object_or_404(Assignment, pk=assignment_id)
        feedback_survey = FeedbackSurvey.objects.get(assignment=assignment)
        survey_template = feedback_survey.template
        context = {
            'course_id': course_id,
            'assignment_id': assignment_id,
            'survey_template_name': survey_template.name,
            'survey_template_instruction': survey_template.instructions,
            'survey_template_other_info': survey_template.other_info,
            'feedback_survey_date_released': feedback_survey.date_released,
            'feedback_survey_date_due': feedback_survey.date_due
        }
        return render(request, 'edit_survey_template.html', context)


def test(request):
    user = request.user
    return render(request, 'test.html')


def test_survey_template(request):
    user = request.user
    return render(request, 'test-survey-template.html')


@login_required
@user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA])
def edit_survey(request, course_id, assignment_id):
    if request.method == 'GET':
        assignment = get_object_or_404(Assignment, pk=assignment_id)
        feedback_survey = get_object_or_404(
            FeedbackSurvey, assignment=assignment)
        survey_template = feedback_survey.template.pk
        return render(request, 'edit_survey.html', {'survey_pk': survey_template, 'course_id': course_id, 'assignment_id': assignment_id})
    else:
        return render(request, 'edit_survey.html')


@login_required
@user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA])
def edit_preview_survey(request, course_id, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    feedback_survey = get_object_or_404(
        FeedbackSurvey, assignment=assignment)
    survey_template = feedback_survey.template.pk
    return render(request, 'edit_preview_survey.html', {'survey_pk': survey_template})


@login_required
@user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA, Registration.UserRole.Student])
def fill_survey(request, course_id, assignment_id, artifact_review_id):
    user = request.user
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    artifact = ArtifactReview.objects.get(
        pk=artifact_review_id).artifact.file
    feedback_survey = get_object_or_404(
        FeedbackSurvey, assignment=assignment)
    survey_template = feedback_survey.template.pk
    return render(request, 'fill_survey.html', {'survey_pk': survey_template, 'artifact_review_pk': artifact_review_id, 'course_id': course_id, 'assignment_id': assignment_id, 'picture': artifact})


def test_report(request):
    return render(request, 'test-report.html')


def report(request, course_id, assignment_id, andrew_id):
    # user = request.user
    user = get_object_or_404(CustomUser, andrew_id=andrew_id)
    course = get_object_or_404(Course, pk=course_id)
    registration = get_object_or_404(
        Registration, users=user, courses=course)
    userRole = registration.userRole
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    assignment_type = assignment.assignment_type
    if assignment_type == "Individual":
        try:
            entity = Individual.objects.get(
                registration=registration, course=course)
            team_name = str(andrew_id)
        except Individual.DoesNotExist:
            # Create an Individual entity for the user
            individual = Individual(course=course)
            individual.save()
            membership = Membership(student=registration, entity=individual)
            membership.save()
            entity = Individual.objects.get(
                registration=registration, course=course)
            team_name = str(andrew_id)
    elif assignment_type == "Team":
        try:
            entity = Team.objects.get(registration=registration, course=course)
            team_name = entity.name
        except Team.DoesNotExist:
            # TODO: Alert: you need to be a member of the team to upload the artifact
            return redirect('assignment', course_id)
    else:
        return redirect('assignment', course_id)
    # find artifact id with assignment id and entity id
    artifact = get_object_or_404(
        Artifact, assignment=assignment, entity=entity)
    artifact_id = artifact.pk
    artifact_path = artifact.file.url
    # artifact_id = Artifact.objects.get(assignment=assignment, entity=entity).pk
    artifact_url = r"/api/artifacts/" + str(artifact_id) + "/"
    print("artifact_url: " + artifact_url)
    print("team_name: " + team_name)
    context = {'user': user,
               'course': course,
               'entity': entity,
               'userRole': userRole,
               'artifact_url': artifact_url,
               'artifact_path': artifact_path,
               'team_name': team_name,
               }
    return render(request, 'test-report.html', context)


@login_required
def course_list(request):
    def get_registrations(user):
        registration = []
        for reg in Registration.objects.filter(users=user):
            if reg.userRole == Registration.UserRole.Student and reg.courses.visible == False:
                continue
            else:
                registration.append(reg)
        return registration

    if request.method == 'GET':
        form = CourseForm(label_suffix='')
        registration = get_registrations(request.user)
        context = {'registration': registration, 'form': form}
        return render(request, 'course.html', context)
    if request.method == 'POST':
        if request.user.is_staff:
            form = CourseForm(request.POST, label_suffix='')
            if form.is_valid():
                course = form.save()
                registration = Registration(
                    users=request.user, courses=course, userRole=Registration.UserRole.Instructor)
                registration.save()
        else:
            form = CourseForm(label_suffix='')

        # registration = get_registrations(request.user)
        # context = {'registration': registration, 'form': form}
        # return render(request, 'course.html', context)
        return redirect('edit_course', course.id)


@login_required
@user_role_check(user_roles=Registration.UserRole.Instructor)
def delete_course(request, course_id):
    if request.method == 'GET':
        course = get_object_or_404(Course, pk=course_id)
        course.delete()
        return redirect('course')
    else:
        return redirect('course')


@login_required
@user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA])
def edit_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES,
                          instance=course, label_suffix='')

        if form.is_valid():
            course = form.save()
        return redirect('course')

    else:
        form = CourseForm(instance=course)
        return render(request, 'edit_course.html', {'course': course, 'form': form})


@login_required
@user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA, Registration.UserRole.Student])
def view_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'GET':

        registration = get_object_or_404(
            Registration, users=request.user, courses=course)

        if course.visible == False and registration.userRole == Registration.UserRole.Student:
            return redirect('course')

        context = {'course': course}
        return render(request, 'view_course_detail.html', context)
    else:
        return redirect('course')


#


@login_required
@user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA, Registration.UserRole.Student])
def member_list(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    # TODO: rethink about permission control for staff(superuser) and instructor
    registration = get_object_or_404(
        Registration, users=request.user, courses=course)
    userRole = registration.userRole

    def get_member_list(course_id):
        registration = Registration.objects.filter(courses=course)
        membership = []
        for i in registration:
            try:
                get_registration_team = Team.objects.filter(registration=i)
                if len(get_registration_team) > 1:
                    team = get_registration_team[len(
                        get_registration_team) - 1].name
                else:
                    team = Team.objects.get(registration=i).name
            except Team.DoesNotExist:
                team = ''
            membership.append({
                'andrew_id': i.users.andrew_id,
                'userRole': i.userRole,
                'team': team,
                'is_activated': i.users.is_activated,
            })
        membership = sorted(membership, key=lambda x: x['team'])
        context = {'membership': membership,
                   'course_id': course_id, 'userRole': userRole}
        return context

    # Create registration for user who is not registered this course, otherwise, return the registration
    def get_users_registration(users, request):
        andrew_id = request.POST['andrew_id']
        role = request.POST['membershipRadios']
        if user not in users:
            registration = Registration(
                users=user, courses=course, userRole=role)
            registration.save()
            message_info = 'A new member has been added'
            assignments = []
            for a in Assignment.objects.filter(course=course, assignment_type=Assignment.AssigmentType.Individual):
                if a.date_due != None and a.date_due < datetime.now().replace(tzinfo=LA):
                    assignments.append(a)
                elif a.date_due == None:
                    assignments.append(a)
            for assignment in assignments:
                artifacts = Artifact.objects.filter(assignment=assignment)
                for artifact in artifacts:
                    artifact_review = ArtifactReview(
                        artifact=artifact, user=registration)
                    artifact_review.save()
        else:
            registration = get_object_or_404(
                Registration, users=user, courses=course)
            registration.userRole = role
            registration.save()

            message_info = andrew_id + '\'s team has been added or updated'
        return registration, message_info

    # Create membership for user's team
    def get_users_team(registration, request):
        team_name = request.POST['team_name']
        if team_name != '' and registration.userRole == 'Student':
            membership = Membership.objects.filter(student=registration)
            if len(membership) == 1:
                team = Team.objects.filter(
                    registration=registration, course=course)
                if len(team) == 1:
                    team = team[0]

                members = team.members
                if len(members) == 1:
                    team.delete()
                else:
                    # add artifact_review for previous team
                    artifacts = Artifact.objects.filter(entity=team)
                    for artifact in artifacts:
                        artifact_review = ArtifactReview(
                            artifact=artifact, user=registration)
                        artifact_review.save()
            membership.delete()
            try:
                team = Team.objects.get(
                    course=course, name=team_name)
                print('1123112', team)
            except Team.DoesNotExist:
                team = Team(course=course, name=team_name)
                team.save()
            membership = Membership(
                student=registration, entity=team)
            membership.save()
            # delete artifact review for updated team
            artifacts = Artifact.objects.filter(entity=team)
            for artifact in artifacts:
                artifact_reviews = ArtifactReview.objects.filter(
                    artifact=artifact, user=registration)
                for artifact_review in artifact_reviews:
                    artifact_review.delete()

    # Create a list of users in the course

    def add_users_from_the_same_course():
        users = []
        users.extend(course.students)
        users.extend(course.TAs)
        users.extend(course.instructors)
        return users

    # Delete ta and instructor membership if he/she is student before
    def delete_memebership_after_switch_to_TA_or_instructor(registration):
        if registration.userRole == 'TA' or registration.userRole == 'Instructor':
            membership = Membership.objects.filter(student=registration)
            if len(membership) == 1:
                team = Team.objects.filter(
                    registration=registration, course=course)
                if len(team) == 1:
                    team = team[0]
                members = team.members
                if len(members) == 1:
                    team.delete()
            membership.delete()
            # delete all artifact_review of TA or instructor
            artifact_reviews = ArtifactReview.objects.filter(user=registration)
            for artifact_review in artifact_reviews:
                artifact_review.delete()

    if request.method == 'GET':
        context = get_member_list(course_id)
        return render(request, 'course_member.html', context)
    elif request.method == 'POST' and userRole != 'Student':
        andrew_id = request.POST['andrew_id']
        try:
            user = CustomUser.objects.get(andrew_id=andrew_id)
            users = add_users_from_the_same_course()
            registration, message_info = get_users_registration(
                users, request)
            delete_memebership_after_switch_to_TA_or_instructor(
                registration)
            get_users_team(registration, request)
        except CustomUser.DoesNotExist:
            message_info = 'AndrewID does not exist'
        messages.info(request, message_info)
        context = get_member_list(course_id)
        return render(request, 'course_member.html', context)
    else:
        return redirect('member_list', course_id)


@login_required
@user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA])
def delete_member(request, course_id, andrew_id):
    if request.method == 'GET':
        user = get_object_or_404(CustomUser, andrew_id=andrew_id)
        registration = get_object_or_404(
            Registration, users=user, courses=course_id)
        membership = Membership.objects.filter(student=registration)
        membership.delete()
        registration.delete()
        return redirect('member_list', course_id)
    else:
        return redirect('member_list', course_id)


@login_required
@user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA, Registration.UserRole.Student])
def assignment(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    userRole = Registration.objects.get(
        users=request.user, courses=course).userRole
    if request.method == 'GET':
        if userRole == Registration.UserRole.Student:
            infos = Assignment.objects.filter(course=course)
            assignments = []
            for assignment in infos:
                if assignment.date_released != None and assignment.date_released.astimezone(pytz.timezone('America/Los_Angeles')) <= datetime.now().replace(tzinfo=LA):
                    assignments.append(assignment)
                elif assignment.date_released == None:
                    assignments.append(assignment)
        else:
            assignments = Assignment.objects.filter(course=course)
        info = []
        for a in assignments:
            feedback_survey = FeedbackSurvey.objects.filter(assignment=a)
            assign = dict()
            assign['assignment'] = a
            assign['feedback_survey'] = feedback_survey.count()
            info.append(assign)
        context = {'infos': info,
                   "course_id": course_id,
                   "course": course,
                   "userRole": userRole}
        return render(request, 'assignment.html', context)

    else:
        form = AssignmentForm(request.POST, label_suffix='')
        if form.is_valid():
            assignment = form.save()
        assignments = Assignment.objects.filter(course=course)
        return redirect('edit_assignment', course_id, assignment.id)


@login_required
@user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA])
def delete_assignment(request, course_id, assignment_id):
    if request.method == 'GET':
        assignment = get_object_or_404(Assignment, pk=assignment_id)
        assignment.delete()
        return redirect('assignment', course_id)
    else:
        return redirect('assignment', course_id)


@login_required
@user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA])
def edit_assignment(request, course_id, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    userRole = Registration.objects.get(
        users=request.user, courses=course_id).userRole
    if request.method == 'POST':
        form = AssignmentForm(
            request.POST, instance=assignment, label_suffix='')

        if form.is_valid():
            # TO-DO: update upload_time
            assignment = form.save()
        return redirect('assignment', course_id)

    if request.method == 'GET':
        form = AssignmentForm(instance=assignment)
        return render(request, 'edit_assignment.html', {'course_id': course_id, 'form': form, 'userRole': userRole})

    else:
        return redirect('assignment', course_id)


@login_required
@user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA, Registration.UserRole.Student])
def view_assignment(request, course_id, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    userRole = Registration.objects.get(
        users=request.user, courses=course_id).userRole
    registration = get_object_or_404(
        Registration, users=request.user, courses=course_id)
    course = get_object_or_404(Course, pk=course_id)
    andrew_id = request.user.andrew_id
    assignment_type = assignment.assignment_type
    if assignment_type == "Individual":
        try:
            entity = Individual.objects.get(
                registration=registration, course=course)
        except Individual.DoesNotExist:
            # Create an Individual entity for the user
            individual = Individual(course=course)
            individual.save()
            membership = Membership(student=registration, entity=individual)
            membership.save()
            entity = Individual.objects.get(
                registration=registration, course=course)
    elif assignment_type == "Team":
        try:
            entity = Team.objects.get(registration=registration, course=course)
        except Team.DoesNotExist:
            # TODO: Alert: you need to be a member of the team to upload the artifact
            print("you need to be a member of the team to upload the artifact")
            return redirect('assignment', course_id)
    else:
        return redirect('assignment', course_id)

    try:
        artifacts = Artifact.objects.filter(
            assignment=assignment, entity=entity)
        latest_artifact = artifacts.latest('upload_time')
        artifact_id = latest_artifact.id
    except Artifact.DoesNotExist:
        latest_artifact = "None"
        artifact_id = 99999

    assignment_id = assignment.id
    context = {'course_id': course_id,
               'userRole': userRole,
               'assignment': assignment,
               'latest_artifact': latest_artifact,
               'assignment_id': assignment_id,
               'artifact_id': artifact_id,
               'andrew_id': andrew_id}
    return render(request, 'view_assignment.html', context)

# return true if the user is the owner of the artifact


def check_artifact_permisssion(artifact_id, user):
    artifact = get_object_or_404(Artifact, pk=artifact_id)
    entity = artifact.entity
    members = entity.members
    if user in members:
        return True
    else:
        return False

# TODO: remove redundant code in artifact section to improve performance in the future
# TODO: create a directory for each course_assignment_team to store the files


@login_required
@user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA, Registration.UserRole.Student])
def artifact(request, course_id, assignment_id):
    course = get_object_or_404(Course, pk=course_id)
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    # TODO: rethink about permission control for staff(superuser) and instructor
    registration = get_object_or_404(
        Registration, users=request.user, courses=course)
    userRole = registration.userRole
    # TODO: check the assigment type.
    assignment_type = assignment.assignment_type
    if assignment_type == "Individual":
        try:
            entity = Individual.objects.get(
                registration=registration, course=course)
        except Individual.DoesNotExist:
            # Create an Individual entity for the user
            individual = Individual(course=course)
            individual.save()
            membership = Membership(student=registration, entity=individual)
            membership.save()
            entity = Individual.objects.get(
                registration=registration, course=course)
    elif assignment_type == "Team":
        try:
            entity = Team.objects.get(registration=registration, course=course)
        except Team.DoesNotExist:
            # TODO: Alert: you need to be a member of the team to upload the artifact
            print("you need to be a member of the team to upload the artifact")
            return redirect('assignment', course_id)
    else:
        return redirect('assignment', course_id)

    if request.method == 'POST':
        # if artifact exists, redirect to the artifact page
        if Artifact.objects.filter(assignment=assignment, entity=entity).exists():
            return redirect('artifact', course_id, assignment_id)

        form = ArtifactForm(request.POST, request.FILES, label_suffix='')
        if form.is_valid():
            artifact = form.save()
            if assignment_type == 'Team':
                team_members = [i.pk for i in entity.members]
                registrations = [i for i in Registration.objects.filter(
                    courses=course) if i.users.pk not in team_members]
                for registration in registrations:
                    if registration.userRole == Registration.UserRole.Student:
                        artifact_review = ArtifactReview(
                            artifact=artifact, user=registration)
                        artifact_review.save()
            else:
                registrations = [i for i in Registration.objects.filter(
                    courses=course) if i.id != registration.id]
                if registration.userRole == Registration.UserRole.Student:
                    for single_registration in registrations:
                        artifact_review = ArtifactReview(
                            artifact=artifact, user=single_registration)
                        artifact_review.save()
        else:
            print("form is not valid")
        artifacts = Artifact.objects.filter(
            assignment=assignment, entity=entity)
        context = {'artifacts': artifacts,
                   "course_id": course_id,
                   "assignment_id": assignment_id,
                   "course": course,
                   "userRole": userRole,
                   "assignment": assignment,
                   "entity": entity}
        return render(request, 'artifact.html', context)

    if request.method == 'GET':
        artifacts = Artifact.objects.filter(
            assignment=assignment, entity=entity)
        context = {'artifacts': artifacts,
                   "course_id": course_id,
                   "assignment_id": assignment_id,
                   "course": course,
                   "userRole": userRole,
                   "assignment": assignment,
                   "entity": entity}
        return render(request, 'artifact.html', context)

    else:
        return redirect('assignment', course_id)


@login_required
@user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA])
def artifact_admin(request, course_id, assignment_id):
    course = get_object_or_404(Course, pk=course_id)
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    registration = get_object_or_404(
        Registration, users=request.user, courses=course)
    userRole = registration.userRole
    if request.method == 'GET':
        artifacts = Artifact.objects.filter(assignment=assignment)
        context = {'artifacts': artifacts,
                   "course_id": course_id,
                   "course": course,
                   "userRole": userRole,
                   "assignment": assignment}
        return render(request, 'artifact_admin.html', context)


@login_required
@user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA, Registration.UserRole.Student])
def download_artifact(request, course_id, assignment_id, artifact_id):
    if check_artifact_permisssion(artifact_id, request.user):
        artifact = get_object_or_404(Artifact, pk=artifact_id)
        if settings.USE_S3:
            from config.storages import MediaStorage
            storage = MediaStorage()
            filename = artifact.file.name
            filepath = storage.url(filename)
            response = FileResponse(storage.open(filename, 'rb'))
        else:
            filepath = artifact.file.path
            response = FileResponse(open(filepath, 'rb'))
        # TODO: return 404 if file does not exist
        return response
    else:
        return redirect('assignment', course_id)


@login_required
@user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA, Registration.UserRole.Student])
def view_artifact(request, course_id, assignment_id, artifact_id):
    if check_artifact_permisssion(artifact_id, request.user):
        artifact = get_object_or_404(Artifact, pk=artifact_id)
        assignment = get_object_or_404(Assignment, pk=assignment_id)
        return render(request, 'view_artifact.html', {'course_id': course_id, 'assignment_id': assignment_id, 'assignment': assignment, 'artifact': artifact})
    else:
        return redirect('assignment', course_id)


@login_required
@user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA, Registration.UserRole.Student])
def delete_artifact(request, course_id, assignment_id, artifact_id):
    if check_artifact_permisssion(artifact_id, request.user):
        print("check_artifact_permisssion delete_artifact True")
    else:
        return redirect('assignment', course_id)

    if request.method == 'GET':
        artifact = get_object_or_404(Artifact, pk=artifact_id)
        # delete the artifact file first
        artifact.file.delete()
        artifact.delete()
        return redirect('artifact', course_id, assignment_id)
    else:
        return redirect('artifact', course_id, assignment_id)


@login_required
@user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA, Registration.UserRole.Student])
def edit_artifact(request, course_id, assignment_id, artifact_id):
    if check_artifact_permisssion(artifact_id, request.user):
        print("check_artifact_permisssion edit_artifact True")
    else:
        return redirect('assignment', course_id)

    artifact = get_object_or_404(Artifact, pk=artifact_id)
    old_file_path = artifact.file
    userRole = Registration.objects.get(
        users=request.user, courses=course_id).userRole
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    if request.method == 'POST':
        form = ArtifactForm(request.POST, request.FILES,
                            instance=artifact, label_suffix='')
        if form.is_valid():
            # delete the artifact file first
            new_file = os.path.split(str(form.cleaned_data['file']))[1]
            if new_file == "False":
                # delete the artifact if "clear" is selected
                # print("old file deleted, old_file_path:", old_file_path)
                old_file_path.delete()
            artifact = form.save()
        return redirect('artifact', course_id, assignment_id)
        # return render(request, 'edit_artifact.html', {'course_id': course_id, 'assignment_id': assignment_id, 'assignment': assignment, 'form': form, 'userRole': userRole})

    if request.method == 'GET':
        form = ArtifactForm(instance=artifact)
        return render(request, 'edit_artifact.html', {'course_id': course_id, 'assignment_id': assignment_id, 'assignment': assignment, 'form': form, 'userRole': userRole})

    else:
        return redirect('artifact', course_id, assignment_id)


@login_required
@user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA, Registration.UserRole.Student])
def review_survey(request, course_id, assignment_id):
    #team, button_survey
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    assignment = get_object_or_404(Assignment, id=assignment_id, course=course)
    feedback_survey = get_object_or_404(FeedbackSurvey, assignment=assignment)
    assignment_type = assignment.assignment_type
    artifacts = Artifact.objects.filter(assignment=assignment)
    # find artifact_review(registration, )
    registration = get_object_or_404(Registration, users=user, courses=course)
    artifact_reviews = []
    for artifact in artifacts:
        artifact_reviews.extend(ArtifactReview.objects.filter(
            artifact=artifact, user=registration))
    infos = []
    for artifact_review in artifact_reviews:
        artifact_review_with_name = dict()
        artifact = artifact_review.artifact
        feedback_survey_released_date = feedback_survey.date_released.astimezone(
            pytz.timezone('America/Los_Angeles'))
        print(feedback_survey_released_date)

        if feedback_survey_released_date <= datetime.now().replace(tzinfo=LA):
            artifact_review_with_name["artifact_review_pk"] = artifact_review.pk
            artifact_review_with_name["status"] = artifact_review.status
            if assignment_type == "Team":
                entity = artifact.entity
                print(entity, artifact.pk, artifact.file.name)
                team = entity.team
                artifact_review_with_name["name"] = team.name

            else:
                entity = artifact.entity
                name = Membership.objects.get(
                    entity=entity).student.users.name_or_andrew_id()
                artifact_review_with_name["name"] = name
            infos.append(artifact_review_with_name)

    return render(request, 'survey_list.html', {'course_id': course_id, 'assignment_id': assignment_id, 'infos': infos, 'assignment_type': assignment_type})
