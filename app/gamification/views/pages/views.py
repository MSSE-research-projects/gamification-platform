from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.shortcuts import redirect, render
from ...models import Course
from ...models import Registration
from ...models import CustomUser

from ...forms import SignUpForm, ProfileForm, CourseForm, RegistrationForm


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
        form = CourseForm(request.POST, label_suffix='')
        if form.is_valid():
            form.save()
        courses = Course.objects.all()
        context = {'courses': courses}
        return render(request, 'course.html', context)


def delete_course(request, course_id):
    if request.method == 'GET':
        course = Course.objects.get(course_id=course_id)
        course.delete()
        return render(request, 'course.html')
    else:
        return render(request, 'course.html')


def edit_course(request, course_id):
    course = Course.objects.get(course_id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course, label_suffix='')

        if form.is_valid():
            course = form.save()

    else:
        form = CourseForm(instance=course)

    return render(request, 'edit_course.html', {'course': course, 'form': form})


def member_list(request, course_id):
    if request.method == 'GET':
        register = Registration.objects.filter(courses_id=course_id)
        users = []
        for r in register:
            user = CustomUser.objects.get(pk=r.users.pk)
            users.append(user)
        context = {'register': register, 'users' : users}
        return render(request, 'course_member.html', context)
    if request.method == 'POST':
        andrew_id = request.POST['andrew_id']
        role = request.POST['membershipRadios']
        course = Course.objects.get(pk=course_id)
        user = CustomUser.objects.get(andrew_id=andrew_id)
        registration = Registration(users=user, courses=course, userRole = role)
        registration.save()
        register = Registration.objects.filter(courses_id=course_id)
        users = []
        for r in register:
            user = CustomUser.objects.get(pk=r.users.pk)
            users.append(user)
        context = {'register': register, 'users' : users}
        return render(request, 'course_member.html', context)
