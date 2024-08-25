from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, Select, TextInput, Textarea, CheckboxSelectMultiple, DateInput
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from student.models import *


class CohortForm(ModelForm):
    """  """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = CohortModel
        fields = '__all__'
        widgets = {
            'start_date': TextInput(attrs={
                'type': 'date'
            }),
            'end_date': TextInput(attrs={
                'type': 'date'
            })
        }


class StudentForm(ModelForm):
    """  """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })
    
    def clean_email(self):
        """Custom validation for the email field."""
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")
        return email

    class Meta:
        model = StudentsModel
        fields = '__all__'
        widgets = {

        }


class StudentProfileForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = StudentsModel
        fields = ['surname', 'last_name', 'gender', 'mobile', 'image']
        widgets = {

        }



