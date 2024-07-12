from django.contrib.auth.models import Permission
from django.db.models.functions import Lower
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
import json
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from human_resource.models import *
from human_resource.forms import *
from django.db.models import Sum


class HRSettingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = HRSettingModel
    form_class = HRSettingForm
    permission_required = 'human_resource.change_hrsettingmodel'
    success_message = 'Human Resource Setting Updated Successfully'
    template_name = 'human_resource/setting/create.html'

    def dispatch(self, *args, **kwargs):
        setting = HRSettingModel.objects.first()
        if not setting:
            return super(HRSettingCreateView, self).dispatch(*args, **kwargs)
        else:
            return redirect(reverse('hr_setting_edit', kwargs={'pk': setting.pk}))

    def get_success_url(self):
        return reverse('hr_setting_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class HRSettingDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = HRSettingModel
    permission_required = 'human_resource.view_hrsettingmodel'
    fields = '__all__'
    template_name = 'human_resource/setting/detail.html'
    context_object_name = "human_resource_setting"

    def dispatch(self, *args, **kwargs):
        setting = HRSettingModel.objects.first()
        if setting:
            if self.kwargs.get('pk') != setting.id:
                return redirect(reverse('hr_setting_detail', kwargs={'pk': setting.pk}))
            return super(HRSettingDetailView, self).dispatch(*args, **kwargs)
        else:
            return redirect(reverse('hr_setting_create'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class HRSettingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = HRSettingModel
    form_class = HRSettingForm
    permission_required = 'human_resource.change_hrsettingmodel'
    success_message = 'Human Resource Setting Updated Successfully'
    template_name = 'human_resource/setting/create.html'

    def get_success_url(self):
        return reverse('hr_setting_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['human_resource_setting'] = self.object
        return context


class PositionCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Group
    permission_required = 'auth.add_group'
    form_class = PositionForm
    template_name = 'human_resource/position/list.html'
    success_message = 'Position Added Successfully'

    def get_success_url(self):
        return reverse('position_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PositionListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Group
    permission_required = 'auth.view_group'
    fields = '__all__'
    template_name = 'human_resource/position/index.html'
    context_object_name = "position_list"

    def get_queryset(self):
        return Group.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PositionForm
        return context


class PositionDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Group
    permission_required = 'auth.view_group'
    fields = '__all__'
    template_name = 'human_resource/position/detail.html'
    context_object_name = "position"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PositionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Group
    permission_required = 'auth.change_group'
    form_class = PositionForm
    template_name = 'human_resource/position/index.html'
    success_message = 'Position Successfully Updated'

    def get_success_url(self):
        return reverse('position_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['position'] = self.object
        context['position_list'] = Group.objects.all().order_by('name')
        return context


class PositionPermissionView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Group
    permission_required = 'auth.change_group'
    form_class = PositionForm
    template_name = 'human_resource/position/permission.html'
    success_message = 'Position Permission Successfully Updated'

    def get_success_url(self):
        return reverse('position_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['position'] = self.object
        context['permission_list'] = Permission.objects.all()
        return context


@login_required
@permission_required('auth.change_group')
def position_permission_view(request, pk):
    position = Group.objects.get(pk=pk)
    if request.method == 'POST':
        permissions = request.POST.getlist('permissions[]')
        permission_list = []
        for permission_code in permissions:
            permission = Permission.objects.filter(codename=permission_code).first()
            if permission:
                permission_list.append(permission.id)
        position.permissions.set(permission_list)
        messages.success(request, 'Position Permission Successfully Updated')
        return redirect(reverse('position_index'))
    context = {
        'position': position,
        'permission_codenames': position.permissions.all().values_list('codename', flat=True),
        'permission_list': Permission.objects.all(),

    }
    return render(request, 'human_resource/position/permission.html', context)


class PositionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Group
    permission_required = 'auth.delete_group'
    fields = '__all__'
    template_name = 'human_resource/position/delete.html'
    context_object_name = "position"

    def get_success_url(self):
        return reverse('position_index')

    def dispatch(self, *args, **kwargs):
        if self.request.POST.get('name'):
            if self.request.POST.get('name').lower() in ['trainer']:
                messages.error(self.request, 'Restricted Position, Permission Denied')
                return redirect(reverse('position_index'))
        return super(PositionDeleteView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class StaffCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = StaffModel
    permission_required = 'human_resource.add_staffmodel'
    form_class = StaffForm
    template_name = 'human_resource/staff/create.html'
    success_message = 'Staff Successfully Registered'

    def get_success_url(self):
        return reverse('staff_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['staff_setting'] = HRSettingModel.objects.filter().first()
        return context


class StaffListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = StaffModel
    permission_required = 'human_resource.view_staffmodel'
    fields = '__all__'
    template_name = 'human_resource/staff/index.html'
    context_object_name = "staff_list"

    def get_queryset(self):
        return StaffModel.objects.all().order_by(Lower('first_name'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class StaffDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = StaffModel
    permission_required = 'human_resource.view_staffmodel'
    fields = '__all__'
    template_name = 'human_resource/staff/detail.html'
    context_object_name = "staff"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class StaffUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = StaffModel
    permission_required = 'human_resource.change_staffmodel'
    form_class = StaffEditForm
    template_name = 'human_resource/staff/edit.html'
    success_message = 'Staff Information Successfully Updated'

    def get_success_url(self):
        return reverse('staff_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['staff_setting'] = HRSettingModel.objects.filter().first()
        context['staff'] = self.object
        return context


class StaffDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = StaffModel
    permission_required = 'human_resource.delete_staffmodel'
    fields = '__all__'
    template_name = 'human_resource/staff/delete.html'
    context_object_name = "staff"
    success_message = 'Staff Successfully Deleted'

    def get_success_url(self):
        return reverse('staff_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
