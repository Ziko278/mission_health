from django.forms import ModelForm, Select, TextInput, DateInput, CheckboxSelectMultiple
from communication.models import *


class SMTPConfigurationForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'is_general' and field != 'use_tls':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = SMTPConfigurationModel
        fields = '__all__'
        widgets = {
            'password': TextInput(attrs={
                'type': 'password'
            })
        }


class CommunicationSettingForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'auto_save_sent_message':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = CommunicationSettingModel
        fields = '__all__'
        widgets = {
            'password': TextInput(attrs={
                'type': 'password'
            })
        }


class MessageForm(ModelForm):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = MessageModel
        fields = '__all__'
        widgets = {

        }


class StudentMessageForm(ModelForm):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = StudentMessageModel
        fields = '__all__'
        widgets = {

        }

