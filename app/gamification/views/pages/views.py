from django.contrib.auth import login
from django.shortcuts import redirect, render
from ...models import user
from ...forms import SignUpForm, ProfileForm


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


# user: andrew_id, first_name, last_name, email, image, is_staff, is_active
# form:Email address, First name, Last name, Profile picture
def profile(request):
    user = request.user
    if(user.is_anonymous):
        print("anonymous user: ", user.andrew_id)
    else:
        print("not anony user: ", user.andrew_id)
    # print(request.FILES)):
    print(user.image)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES,
                           instance=user, label_suffix='')
        
        if form.is_valid():
            user = form.save()
            # message.success(request, f'Your account has been updated')
    # print(user, type(user), user.andrew_id)
    else:
        form = ProfileForm(instance=user)
    print("form:    ", form)
    return render(request, 'profile.html', {'user': user, 'form': form})

def test(request):
    user = request.user
    return render(request, 'test.html', {'user': user})