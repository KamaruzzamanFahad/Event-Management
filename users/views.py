from django.shortcuts import render
from users.forms import SignUpForm, SignInForm
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import Group
# Create your views here.

def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.groups.add(Group.objects.get(name='Participant'))
            user.save()
            messages.success(request, 'Please Check Your Email to Confirm Your Account!')
            return redirect('signin')
        else:
            messages.error(request, 'Something went wrong!, Please Check Details')
    return render(request, 'signup.html', {'form': form})

def signin(request):
    form = SignInForm()
    if request.method == 'POST':
        form = SignInForm(request=request, data=request.POST)
        print("request hit")
        if form.is_valid():
            print("form is valid")
            user = form.get_user()
            print("user", user)
            login(request, user)
            messages.success(request, 'You are logged in successfully!')
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            # messages.error(request, f'Error: {form.errors}')
            # messages.error(request, f'Invalid Credentials or Account Not Activated, Please Check Your Email to Confirm Your Account!, {form.errors }')
    return render(request, 'signin.html', {'form': form})

def signout(request):
    logout(request)
    messages.success(request, 'You are logged out successfully!')
    return redirect('signin')


def activate(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'Invalid User!')
        return redirect('signin')
    
    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated successfully!')
        return redirect('signin')
    else:
        messages.error(request, 'Invalid Token!')
        return redirect('signin')
        

