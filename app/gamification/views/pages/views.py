from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from ...forms import AssignmentForm, SignUpForm, ProfileForm, CourseForm, TeamForm
from ...models import Assignment, Course, CustomUser, Registration, Entity, Team


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
    if request.method == 'GET':
        courses = Course.objects.all()
        context = {'courses': courses}
        return render(request, 'course.html', context)
    if request.method == 'POST':
        form = CourseForm(request.POST, label_suffix='')
        if form.is_valid():
            print('form is valid')
            form.save()
        print(form.errors)
        courses = Course.objects.all()
        context = {'courses': courses}
        return render(request, 'course.html', context)


@login_required
def delete_course(request, course_id):
    # TODO: Use 'DELETE' method to delete course
    if request.method == 'GET':
        course = Course.objects.get(pk=course_id)
        course.delete()
        return redirect('course')
    else:
        return redirect('course')


@login_required
def edit_course(request, course_id):
    course = Course.objects.get(pk=course_id)
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
def member_list(request, course_id):

    def get_member_list(course_id):
        register = Registration.objects.filter(courses_id=course_id)
        users = []
        for r in register:
            user = CustomUser.objects.get(pk=r.users.pk)
            users.append(user)
        context = {'register': register, 'users': users}
        return context

    if request.method == 'GET':
        context = get_member_list(course_id)
        return render(request, 'course_member.html', context)

    if request.method == 'POST':
        andrew_id = request.POST['andrew_id']
        role = request.POST['membershipRadios']
        course = Course.objects.get(pk=course_id)
        user = CustomUser.objects.get(andrew_id=andrew_id)
        exist_user = len(Registration.objects.filter(users=user))
        if exist_user == 0:
            registration = Registration(
                users=user, courses=course, userRole=role)
            registration.save()
            context = get_member_list(course_id)
            return render(request, 'course_member.html', context)
        else:
            context = get_member_list(course_id)
            return render(request, 'course_member.html', context)


@login_required
def assignment(request, course_id):
    course = Course.objects.get(pk=course_id)

    if request.method == 'GET':
        assignments = Assignment.objects.filter(course=course)
        context = {'assignments': assignments, "course_id": course_id}
        return render(request, 'assignment.html', context)

    if request.method == 'POST':
        form = AssignmentForm(request.POST, label_suffix='')
        if form.is_valid():
            form.save()
        assignments = Assignment.objects.filter(course=course)
        context = {'assignments': assignments, "course_id": course_id}
        return render(request, 'assignment.html', context)


@login_required
def delete_assignment(request, course_id, assignment_id):
    # TODO: Use 'DELETE' method to delete assignment
    if request.method == 'GET':
        assignment = Assignment.objects.get(id=assignment_id)
        assignment.delete()
        return redirect('assignment', course_id)
    else:
        return redirect('assignment', course_id)


@login_required
def edit_assignment(request, course_id, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)
    if request.method == 'POST':
        form = AssignmentForm(
            request.POST, instance=assignment, label_suffix='')

        if form.is_valid():
            assignment = form.save()

    else:
        form = AssignmentForm(instance=assignment)

    return render(request, 'edit_assignment.html', {'course_id': course_id, 'form': form})


@login_required
def team(request):
    if request.method == 'GET':
        teams = Team.objects.all()
        entities = Entity.objects.all()
        context = {'teams': teams, 'entities': entities}
        return render(request, 'team.html', context)
    if request.method == 'POST':
        form = TeamForm(request.POST, label_suffix='')
        if form.is_valid():
            form.save()
        teams = Team.objects.all()
        context = {'teams': teams}
        return render(request, 'team.html', context)
