from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User 
from events.forms import StyleFormMixin



class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'border p-2 w-full mb-4', 'placeholder': 'Username'})
        self.fields['first_name'].widget.attrs.update({'class': 'border p-2 w-full mb-4', 'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'class': 'border p-2 w-full mb-4', 'placeholder': 'Last Name'})
        self.fields['email'].widget.attrs.update({'class': 'border p-2 w-full mb-4', 'placeholder': 'Email'})
        self.fields['password1'].widget.attrs.update({'class': 'border p-2 w-full mb-4', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'border p-2 w-full mb-4', 'placeholder': 'Confirm Password'})
        for fieldname in ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
        

class SignInForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(SignInForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'border p-2 w-full mb-4', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class': 'border p-2 w-full mb-4', 'placeholder': 'Password'}) 
        for fieldname in ['username', 'password']:
            self.fields[fieldname].help_text = None