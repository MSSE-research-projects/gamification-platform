import os
from ctypes import sizeof
from hashlib import new
from webbrowser import get
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.http import FileResponse

from app.gamification.decorators import admin_required, user_role_check
from app.gamification.forms import AssignmentForm, SignUpForm, ProfileForm, CourseForm, PasswordResetForm, ArtifactForm
from app.gamification.models import Assignment, Course, CustomUser, Registration, Team, Membership, Artifact, Entity, Individual
from app.gamification.models.artifact_review import ArtifactReview
from .survey_views import *


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

    if request.method == 'GET':
        andrew_id = request.user.andrew_id
        form = CourseForm(label_suffix='')
        unsorted_registration = get_registrations(request.user)
        # TODO: sort registration by semester in a better way
        registration = sorted(unsorted_registration,
                              key=lambda x: x.courses.semester, reverse=True)
        context = {'registration': registration,
                   'form': form, 'andrew_id': andrew_id}
        return render(request, 'dashboard.html', context)


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


def test(request):
    user = request.user
    return render(request, 'test.html')


def test_survey_template(request):
    user = request.user
    return render(request, 'test-survey-template.html')


def test_add_survey(request):
    user = request.user
    return render(request, 'test-add-survey.html', {'survey_pk': 1})


def test_preview_survey(request):
    user = request.user
    return render(request, 'test-preview-survey.html', {'survey_pk': 1})


def test_fill_survey(request):
    user = request.user
    return render(request, 'test-fill-survey.html', {'survey_pk': 1, 'artifact_review_pk': 1})


def report(request, course_id, andrew_id):
    # user = request.user
    user = get_object_or_404(CustomUser, andrew_id=andrew_id)
    course = get_object_or_404(Course, pk=course_id)
    registration = get_object_or_404(
        Registration, users=user, courses=course)
    userRole = registration.userRole
    try:
        entity = Team.objects.get(registration=registration, course=course)
    except Team.DoesNotExist:
        try:
            entity = Individual.objects.get(
                registration=registration, course=course)
        except Individual.DoesNotExist:
            # Create an Individual entity for the user
            print("Team does not exist, create an individual entity for the user")
            individual = Individual(course=course)
            individual.save()
            membership = Membership(student=registration, entity=individual)
            membership.save()
            entity = Individual.objects.get(
                registration=registration, course=course)

    # 'name': chart_type + "-" + unique_name(use number here)
    card1 = {'title': "title0", 'name': "pieChart-0", 'areaData': []}
    card2 = {'title': "title1", 'name': "pieChart-1", 'areaData': []}
    card3 = {'title': "title2", 'name': "pieChart-2", 'areaData': []}
    row = []
    row.append(card1)
    row.append(card2)
    row.append(card3)
    card4 = {'title': "title3", 'name': "pieChart-3", 'areaData': []}
    card5 = {'title': "title4", 'name': "pieChart-4", 'areaData': []}
    card6 = {'title': "title5", 'name': "pieChart-5", 'areaData': []}
    row2 = []
    row2.append(card4)
    row2.append(card5)
    row2.append(card6)
    section = []
    section_name = "Software Engineering Problem"
    section.append(section_name)
    section.append(row)
    section.append(row2)

    card7 = {'title': "title6", 'name': "areaChart", 'areaData': []}
    card8 = {'title': "title7", 'name': "lineChart", 'areaData': []}
    card9 = {'title': "title8", 'name': "barChart", 'areaData': []}
    card11 = {'title': "title10", 'name': "scatterChart", 'areaData': []}
    row = []
    row.append(card7)
    row.append(card8)
    row.append(card9)
    row.append(card11)
    section2 = []
    section_name2 = "Software Engineering Problem2"
    section2.append(section_name2)
    section2.append(row)

    sections = []
    sections.append(section)
    sections.append(section2)
    #
    score_list = []
    score1 = {'name': 'Content', 'value': 8.00, 'max_value': 10.00}
    score2 = {'name': 'Design', 'value': 6.00, 'max_value': 10.00}
    score3 = {'name': 'Delivery', 'value': 4.00, 'max_value': 10.00}
    score4 = {'name': 'Overall', 'value': 6.00, 'max_value': 10.00}
    score_list.append(score1)
    score_list.append(score2)
    score_list.append(score3)
    score_list.append(score4)
    final_score = 'A-'
    #
    context = {'user': user, 'course': course, 'entity': entity, 'userRole': userRole,
               'sections': sections, 'score_list': score_list, 'final_score': final_score}
    return render(request, 'report.html', context)


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

        registration = get_registrations(request.user)
        context = {'registration': registration, 'form': form}
        return render(request, 'course.html', context)


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

    def get_users_registration(users, request):
        andrew_id = request.POST['andrew_id']
        role = request.POST['membershipRadios']
        if user not in users:
            registration = Registration(
                users=user, courses=course, userRole=role)
            registration.save()
            message_info = 'A new mamber has been added'
        else:
            registration = get_object_or_404(
                Registration, users=user, courses=course)
            registration.userRole = role
            registration.save()
            message_info = andrew_id + '\'s team has been added or updated'
        return registration, message_info

    def get_users_team(registration, request):
        team_name = request.POST['team_name']
        if team_name != '' and registration.userRole == 'Student':
            try:
                team = Team.objects.get(
                    course=course, name=team_name)
            except Team.DoesNotExist:
                team = Team(course=course, name=team_name)
                team.save()
            membership = Membership(
                student=registration, entity=team)
            membership.save()

    def add_users_from_the_same_course():
        users = []
        users.extend(course.students)
        users.extend(course.TAs)
        users.extend(course.instructors)
        return users

    def delete_memebership_after_switch_to_TA_or_instructor(registration):
        if registration.userRole == 'TA' or registration.userRole == 'Instructor':
            membership = Membership.objects.filter(student=registration)
            if len(membership) == 1:
                team = Team.objects.filter(registration=registration)
                team.delete()
            membership.delete()

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
        assignments = Assignment.objects.filter(course=course)
        context = {'assignments': assignments,
                   "course_id": course_id,
                   "course": course,
                   "userRole": userRole}
        return render(request, 'assignment.html', context)

    if request.method == 'POST':
        # redirect if user is student
        if userRole == 'Student':
            return redirect('assignment', course_id)

        form = AssignmentForm(request.POST, label_suffix='')
        if form.is_valid():
            form.save()
        assignments = Assignment.objects.filter(course=course)
        context = {'assignments': assignments,
                   "course_id": course_id,
                   "course": course,
                   "userRole": userRole}
        return render(request, 'assignment.html', context)

    else:
        return redirect('assignment', course_id)


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
        return render(request, 'edit_assignment.html', {'course_id': course_id, 'form': form, 'userRole': userRole})

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
    try:
        entity = Team.objects.get(registration=registration, course=course)
    except Team.DoesNotExist:
        try:
            entity = Individual.objects.get(
                registration=registration, course=course)
        except Individual.DoesNotExist:
            # Create an Individual entity for the user
            print("Team does not exist, create an individual entity for the user")
            individual = Individual(course=course)
            individual.save()
            membership = Membership(student=registration, entity=individual)
            membership.save()
            entity = Individual.objects.get(
                registration=registration, course=course)

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
               'artifact_id': artifact_id}
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
    print("assignment_type: " + assignment_type)
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
        form = ArtifactForm(request.POST, request.FILES, label_suffix='')
        if form.is_valid():
            artifact = form.save()
            if assignment_type == 'Team':
                team_members = [i.pk for i in entity.members]
                registrations = [i for i in Registration.objects.filter(
                     courses=course) if i.users.pk not in team_members]
                for registration in registrations:
                    artifact_review = ArtifactReview(
                        artifact=artifact, user=registration)
                    artifact_review.save()
            else:
                registrations = [i for i in Registration.objects.filter(
                    courses=course) if i.id != registration.id]
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
        filename = artifact.file.path
        response = FileResponse(open(filename, 'rb'))
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
        return render(request, 'edit_artifact.html', {'course_id': course_id, 'assignment_id': assignment_id, 'assignment': assignment, 'form': form, 'userRole': userRole})

    if request.method == 'GET':
        form = ArtifactForm(instance=artifact)
        return render(request, 'edit_artifact.html', {'course_id': course_id, 'assignment_id': assignment_id, 'assignment': assignment, 'form': form, 'userRole': userRole})

    else:
        return redirect('artifact', course_id, assignment_id)
