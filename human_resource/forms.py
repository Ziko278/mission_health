from django.forms import ModelForm, Select, TextInput, DateInput, CheckboxInput, CheckboxSelectMultiple
from human_resource.models import *


class StaffForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].queryset = Group.objects.all().order_by('name')

        for field in self.fields:
            if field != 'is_trainer':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = StaffModel
        fields = '__all__'
        widgets = {
            'date_of_birth': DateInput(attrs={
                'type': 'date'
            }),
            'employment_date': DateInput(attrs={
                'type': 'date'
            }),

        }


class StaffEditForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].queryset = Group.objects.all().order_by('name')
        for field in self.fields:
            if field != 'is_trainer':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = StaffModel
        exclude = []
        widgets = {
            'date_of_birth': DateInput(attrs={
                'type': 'date'
            }),
            'employment_date': DateInput(attrs={
                'type': 'date'
            }),
            'staff_id': TextInput(attrs={
                'readonly': True
            }),

        }


class StaffProfileForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = StaffModel
        fields = ['first_name', 'last_name', 'gender', 'address', 'date_of_birth', 'mobile', 'image']
        widgets = {
            'date_of_birth': TextInput({
                'type': 'date'
            })
        }


class HRSettingForm(ModelForm):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field in ['staff_id_prefix']:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = HRSettingModel
        fields = '__all__'
        widgets = {
            'date_obtained': DateInput(attrs={
                'type': 'date'
            }),
        }


class PositionForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = Group
        fields = '__all__'

        widgets = {

        }
