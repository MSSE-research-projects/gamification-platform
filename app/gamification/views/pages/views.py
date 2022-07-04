from curses import use_default_colors
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib import messages
from app.gamification.models import registration

from ...forms import AssignmentForm, SignUpForm, ProfileForm, CourseForm, TeamForm
from ...models import Assignment, Course, CustomUser, Registration, Entity, Team, Membership


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


def signout(request):
    logout(request)
    return redirect('signin')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


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
        form = ProfileForm(instance=user)

    return render(request, 'profile.html', {'user': user, 'form': form})


@login_required
def instructor_admin(request):
    user = request.user
    if user.is_staff:
        return render(request, 'instructor_admin.html')
    else:
        return redirect('dashboard')


def test(request):
    user = request.user
    return render(request, 'test.html', {'user': user})


@login_required
def course(request):
    # TODO: Filter courses by user
    if request.method == 'GET':
        courses = Course.objects.all()
        context = {'courses': courses}
        return render(request, 'course.html', context)
    if request.method == 'POST':
        if request.user.is_staff:
            form = CourseForm(request.POST, label_suffix='')
            if form.is_valid():
                form.save()
        courses = Course.objects.all()
        context = {'courses': courses}
        return render(request, 'course.html', context)

# TODO: Add course detail view


@login_required
def delete_course(request, course_id):
    # TODO: Use 'DELETE' method to delete course
    if request.method == 'GET' and request.user.is_staff:
        course = Course.objects.get(pk=course_id)
        course.delete()
        return redirect('course')
    else:
        return redirect('course')


@login_required
def edit_course(request, course_id):
    course = Course.objects.get(pk=course_id)
    if request.method == 'POST' and request.user.is_staff:
        form = CourseForm(request.POST, request.FILES,
                          instance=course, label_suffix='')

        if form.is_valid():
            course = form.save()

        return redirect('course')

    else:
        form = CourseForm(instance=course)

    return render(request, 'edit_course.html', {'course': course, 'form': form})


@login_required
def member_list(request, course_id):
    
    def get_member_list(course_id):
        course = Course.objects.get(pk=course_id)
        registration = Registration.objects.filter(courses=course)
        membership = []        
        #andrewID, Role, Team
        for i in registration:
            try:
                if len(Team.objects.filter(registration=i)) > 1:
                    team = Team.objects.filter(registration=i)[len(Team.objects.filter(registration=i)) - 1].name
                else:
                    team = Team.objects.get(registration=i).name
            except Team.DoesNotExist:
                team = ''
            membership.append([i.users.andrew_id, i.userRole, team])
        context = {'membership': membership, 'course_id': course_id}
        return context

    if not request.user.is_staff:
        return redirect('course')
    if request.method == 'GET':
        context = get_member_list(course_id)
        return render(request, 'course_member.html', context)
    if request.method == 'POST':
        andrew_id = request.POST['andrew_id']
        role = request.POST['membershipRadios']
        team_name = request.POST['team_name']
        course = Course.objects.get(pk=course_id)
        try:
            user = CustomUser.objects.get(andrew_id=andrew_id)
            users = []
            users.extend(course.students)
            users.extend(course.TAs)
            if user not in users:
                registration = Registration(
                    users=user, courses=course, userRole=role)
                registration.save()
                try:
                    team = Team.objects.get(
                        course=course, name=team_name)
                except Team.DoesNotExist:
                    team = Team(course=course, name=team_name)
                    team.save()
                membership = Membership(student=registration, entity=team)
                membership.save()
                # Re-get all members
                context = get_member_list(course_id)
                messages.info(request, 'A new mamber has been added')
                return render(request, 'course_member.html', context)
            else:
                registration = Registration.objects.get(users=user, courses=course)
                try:
                    team = Team.objects.get(
                        course=course, name=team_name)
                except Team.DoesNotExist:
                    team = Team(course=course, name=team_name)
                    team.save()
                membership = Membership(student=registration, entity=team)
                membership.save()
                context = get_member_list(course_id)
                messages.info(request, andrew_id + '\'s team has been added or updated')
                return render(request, 'course_member.html', context)
        except CustomUser.DoesNotExist:
            messages.info(request, 'Invalid or unexist andrewID')
            context = get_member_list(course_id)
            return render(request, 'course_member.html', context)

@login_required
def delete_member(request, course_id, andrew_id):
    if request.method == 'GET':
        user = CustomUser.objects.get(andrew_id=andrew_id)
        registration = Registration.objects.get(users = user)
        membership = Membership.objects.filter(student = registration)
        membership.delete()
        registration.delete()
        return redirect('member_list', course_id)
    else:
        return redirect('member_list', course_id)


@login_required
def assignment(request, course_id):
    course = Course.objects.get(pk=course_id)

    if request.method == 'GET':
        assignments = Assignment.objects.filter(course=course)
        context = {'assignments': assignments, "course_id": course_id}
        return render(request, 'assignment.html', context)

    if request.method == 'POST' and request.user.is_staff:
        form = AssignmentForm(request.POST, label_suffix='')
        if form.is_valid():
            form.save()
        assignments = Assignment.objects.filter(course=course)
        context = {'assignments': assignments, "course_id": course_id}
        return render(request, 'assignment.html', context)

# TODO: Add assignment detail view


@login_required
def delete_assignment(request, course_id, assignment_id):
    # TODO: Use 'DELETE' method to delete assignment
    if request.method == 'GET' and request.user.is_staff:
        assignment = Assignment.objects.get(id=assignment_id)
        assignment.delete()
        return redirect('assignment', course_id)
    else:
        return redirect('assignment', course_id)


@login_required
def edit_assignment(request, course_id, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)
    if request.method == 'POST' and request.user.is_staff:
        form = AssignmentForm(
            request.POST, instance=assignment, label_suffix='')

        if form.is_valid():
            assignment = form.save()

    else:
        form = AssignmentForm(instance=assignment)

    return render(request, 'edit_assignment.html', {'course_id': course_id, 'form': form})



