from django.contrib.auth import login
from django.shortcuts import redirect, render

from ...forms import SignUpForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, label_suffix='')
        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('dashboard')
    else:
        form = SignUpForm(label_suffix='')

    return render(request, 'signup.html', {'form': form})


def dashboard(request):
    return render(request, 'dashboard.html')

def signin(request):
    if request.method == 'POST':
        return redirect('dashboard')
    else:
        form = SignUpForm(label_suffix='')

    return render(request, 'signin.html', {'form': form})
