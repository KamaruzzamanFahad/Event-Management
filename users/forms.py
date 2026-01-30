from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm

from events.forms import StyleFormMixin

from django.contrib.auth import get_user_model
User = get_user_model()



class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['profile_picture', 'username', 'first_name', 'last_name', 'phone_number', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_picture'].widget.attrs.update({'class': 'border p-2 w-full mb-4', 'placeholder': 'Profile Picture'})
        self.fields['username'].widget.attrs.update({'class': 'border p-2 w-full mb-4', 'placeholder': 'Username'})
        self.fields['first_name'].widget.attrs.update({'class': 'border p-2 w-full mb-4', 'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'class': 'border p-2 w-full mb-4', 'placeholder': 'Last Name'})
        self.fields['phone_number'].widget.attrs.update({'class': 'border p-2 w-full mb-4', 'placeholder': 'Phone Number'})
        self.fields['email'].widget.attrs.update({'class': 'border p-2 w-full mb-4', 'placeholder': 'Email'})
        self.fields['password1'].widget.attrs.update({'class': 'border p-2 w-full mb-4', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'border p-2 w-full mb-4', 'placeholder': 'Confirm Password'})
        for fieldname in ['profile_picture', 'username', 'first_name', 'last_name', 'phone_number', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
        


class SignInForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(SignInForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'border p-2 w-full mb-4', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class': 'border p-2 w-full mb-4', 'placeholder': 'Password'}) 
        for fieldname in ['username', 'password']:
            self.fields[fieldname].help_text = None

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_picture', 'first_name', 'last_name', 'phone_number', 'email']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_picture'].widget = forms.FileInput(attrs={
            'class': 'border p-2 w-full mb-4 bg-gray-50 rounded-lg',
            'accept': 'image/*'
        })
        self.fields['first_name'].widget.attrs.update({'class': 'border p-2 w-full mb-4', 'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'class': 'border p-2 w-full mb-4', 'placeholder': 'Last Name'})
        self.fields['phone_number'].widget.attrs.update({'class': 'border p-2 w-full mb-4', 'placeholder': 'Phone Number'})
        self.fields['email'].widget.attrs.update({'class': 'border p-2 w-full mb-4', 'placeholder': 'Email'})
        for fieldname in ['profile_picture', 'first_name', 'last_name', 'phone_number', 'email']:
            self.fields[fieldname].help_text = None


class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'border p-2 w-full mb-4', 'placeholder': 'Old Password'})
        self.fields['new_password1'].widget.attrs.update({'class': 'border p-2 w-full mb-4', 'placeholder': 'New Password'})
        self.fields['new_password2'].widget.attrs.update({'class': 'border p-2 w-full mb-4', 'placeholder': 'Confirm New Password'})
        for fieldname in ['old_password', 'new_password1', 'new_password2']:
            self.fields[fieldname].help_text = None


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'border p-2 w-full mb-4', 'placeholder': 'Email'})
        for fieldname in ['email']:
            self.fields[fieldname].help_text = None
    

class CustomPasswordResetConfirmForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'class': 'border p-2 w-full mb-4', 'placeholder': 'New Password'})
        self.fields['new_password2'].widget.attrs.update({'class': 'border p-2 w-full mb-4', 'placeholder': 'Confirm New Password'})
        for fieldname in ['new_password1', 'new_password2']:
            self.fields[fieldname].help_text = None