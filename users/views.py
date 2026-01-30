from django.shortcuts import render
from users.forms import SignUpForm, SignInForm, UpdateProfileForm, ChangePasswordForm, CustomPasswordResetForm, CustomPasswordResetConfirmForm
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import Group
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
User = get_user_model()
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy


# Create your views here.

def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
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
        

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'
    login_url = '/users/signin/'


class UpdateProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'update_profile.html'
    login_url = '/users/signin/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UpdateProfileForm(instance=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        form = UpdateProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile', request.user.username)
        else:
            messages.error(request, 'Something went wrong!, Please Check Details')
            return redirect('update_profile')

class ChangePasswordView(LoginRequiredMixin, TemplateView):
    template_name = 'change_password.html'
    login_url = '/users/signin/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ChangePasswordForm(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password changed successfully!')
            return redirect('profile', request.user.username)
        else:
            messages.error(request, f'Something went wrong!, Please Check Details')
            return redirect('change_password', request.user.username)



class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'password_reset.html'
    success_url = reverse_lazy('signin')
    html_email_template_name = 'reset_email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Password reset email sent successfully!')
        return super().form_valid(form)
    

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('signin')
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Password reset successfully!')
        return super().form_valid(form)

    
    