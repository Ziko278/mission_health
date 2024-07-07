from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, Select, TextInput, CheckboxInput, CheckboxSelectMultiple
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from student.models import StudentProfileModel


class SignUpForm(UserCreationForm):

    def clean(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exists():
            raise ValidationError({'email': 'Email Already Exists'})
        if User.objects.filter(username=username).exists():
            raise ValidationError({'username': 'Username Already Exists'})    
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

    class Meta:

        widgets = {
             'password': TextInput(attrs={
                 'class': 'form-control',
                 'type': 'password',
             }),

        }


class ProfileForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'allow_part_payment' and field != 'student_class':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = StudentProfileModel
        fields = '__all__'
        widgets = {
            # 'school': TextInput(attrs={
            #     'class': 'form-control',
            # }),

        }
