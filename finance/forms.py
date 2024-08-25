from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, Select, TextInput, Textarea, CheckboxSelectMultiple, DateInput
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from finance.models import *


class CurrencyForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'use_global':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = CurrencyModel
        fields = '__all__'
        widgets = {

        }


class FinanceSettingForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'auto_confirm_online_payment' and field != 'allow_part_payment':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = FinanceSettingModel
        fields = '__all__'
        widgets = {

        }
        
        
class BankAccountForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'use_global':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = BankAccountModel
        fields = '__all__'
        widgets = {

        }


class OnlinePaymentPlatformForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'use_global':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = OnlinePaymentPlatformModel
        fields = '__all__'
        widgets = {

        }


class TrainingPaymentForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = TrainingPaymentModel
        fields = '__all__'
        widgets = {

        }


class TrainingPaymentEditForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = TrainingPaymentModel
        fields = '__all__'
        exclude = ['type', 'user']
        widgets = {

        }

