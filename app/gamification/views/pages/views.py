from html import entities
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.shortcuts import redirect, render

from app.gamification.models.entity import Entity, Team
from ...models import Course

from ...forms import SignUpForm, ProfileForm, CourseForm, TeamForm


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


def dashboard(request):
    return render(request, 'dashboard.html')


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


def profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES,
                           instance=user, label_suffix='')

        if form.is_valid():
            user = form.save()

    else:
        form = ProfileForm(instance=user)

    return render(request, 'profile.html', {'user': user, 'form': form})


def test(request):
    user = request.user
    return render(request, 'test.html', {'user': user})


def course(request):
    if request.method == 'GET':
        courses = Course.objects.all()
        context = {'courses': courses}
        return render(request, 'course.html', context)
    if request.method == 'POST':
        form = CourseForm(
            request.POST, instance=request.course, label_suffix='')
        if form.is_valid():
            form.save()
        courses = Course.objects.all()
        context = {'courses': courses}
        return render(request, 'course.html', context)
    # else:
    #    courses = []
    #    context = {'courses': courses}
    #    return render(request, 'course.html', context)


def edit_course(request, course_id):
    course = Course.objects.get(course_id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES,
                          instance=course, label_suffix='')

        if form.is_valid():
            course = form.save()

    else:
        form = CourseForm(instance=course)

    return render(request, 'edit_course.html', {'course': course, 'form': form})


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
