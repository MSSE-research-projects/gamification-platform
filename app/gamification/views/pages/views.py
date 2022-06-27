from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.shortcuts import redirect, render
from ...models import Course, Assignment

from ...forms import SignUpForm, ProfileForm, CourseForm, AssignmentForm


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


def assignment(request):
    if request.method == 'GET':
        assignments = Assignment.objects.all()
        context = {'assignments': assignments}
        return render(request, 'assignment.html', context)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, label_suffix='')
        if form.is_valid():
            form.save()
        assignments = Assignment.objects.all()
        context = {'assignments': assignments}
        return render(request, 'assignment.html', context)

def delete_assignment(request, assignment_id):
    if request.method == 'GET':
        assignment = Assignment.objects.get(id=assignment_id)
        assignment.delete()
        return redirect('assignment')
    else:
        return redirect('assignment')

def edit_assignment(request, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment, label_suffix='')

        if form.is_valid():
            assignment = form.save()

    else:
        form = AssignmentForm(instance=assignment)

    return render(request, 'edit_assignment.html', {'assignment': assignment, 'form': form})

# def assignment(request, id):
#     assignment = Assignment.objects.get(id=id)
#     if request.method == 'GET':
#         assignments = Assignment.objects.all()
#         context = {'assignments': assignments}
#         return render(request, 'assignment.html', context)
#     if request.method == 'POST':
#         form = AssignmentForm(request.POST, instance=assignment, label_suffix='')
#         if form.is_valid():
#             form.save()
#         assignments = Assignment.objects.all()
#         context = {'assignments': assignments}
#         return render(request, 'assignment.html', context)