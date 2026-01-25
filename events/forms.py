from django import forms
from events.models import Event, Category, Participant


class StyleFormMixin:
     default_classes = "border p-2 w-full mb-4"

     def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.apply_styles_widgets()

     def apply_styles_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Textarea) or isinstance(field.widget, forms.TextInput) or isinstance(field.widget, forms.SelectDateWidget) or isinstance(field.widget, forms.TimeInput) or isinstance(field.widget, forms.EmailInput) or isinstance(field.widget, forms.Select):
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f' {self.default_classes} {existing_classes}'.strip()

class CreateCategory(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = "name", "description"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter Category Name'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'placeholder': 'Enter Category Description'}),
        }


class CreateEvent(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = "name", "imagelink", "location", "date", "time", "description", "category"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter Event Name'}),
            'imagelink': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter Image Link'}),
            'location': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter Event Location'}),
            'date': forms.SelectDateWidget(attrs={'class': 'form-select'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-input', 'placeholder': 'Enter Event Time'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'placeholder': 'Enter Event Description'}),
            'category': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Select Category'}),
        }

class CreateParticipant(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Participant
        fields = "name", "email", "event"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter Participant Name'}),
            'email': forms.EmailInput(attrs={'type': 'email', 'class': 'form-input', 'placeholder': 'Enter Email Address'}),
            'event': forms.CheckboxSelectMultiple(attrs={'class': 'form-select'}),
        }   