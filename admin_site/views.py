from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin, messages
# from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from communication.models import RecentActivityModel
from student.models import StudentsModel
from admin_site.models import *
from admin_site.forms import *


class AdminDashboardView(TemplateView):
    template_name = 'admin_site/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_activity_list'] = RecentActivityModel.objects.all().order_by('id').reverse()[:10]
        context['active_students'] = StudentsModel.objects.filter(status='active').count()
        return context


class SiteInfoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = SiteInfoModel
    form_class = SiteInfoForm
    permission_required = 'admin_site.change_siteinfomodel'
    success_message = 'Site Information Updated Successfully'
    template_name = 'admin_site/site_info/create.html'

    def dispatch(self, *args, **kwargs):
        site_info = SiteInfoModel.objects.first()
        if not site_info:
            return super(SiteInfoCreateView, self).dispatch(*args, **kwargs)
        else:
            return redirect(reverse('site_info_edit', kwargs={'pk': site_info.pk}))

    def get_success_url(self):
        return reverse('site_info_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SiteInfoDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = SiteInfoModel
    permission_required = 'admin_site.view_siteinfomodel'
    fields = '__all__'
    template_name = 'admin_site/site_info/detail.html'
    context_object_name = "site_info"

    def dispatch(self, *args, **kwargs):
        site_info = SiteInfoModel.objects.first()
        if site_info:
            if self.kwargs.get('pk') != site_info.id:
                return redirect(reverse('site_info_detail', kwargs={'pk': site_info.pk}))
            return super(SiteInfoDetailView, self).dispatch(*args, **kwargs)
        else:
            return redirect(reverse('site_info_create'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class SiteInfoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = SiteInfoModel
    permission_required = 'admin_site.change_siteinfomodel'
    form_class = SiteInfoForm
    success_message = 'Site Information Updated Successfully'
    template_name = 'admin_site/site_info/create.html'

    def get_success_url(self):
        return reverse('site_info_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_info'] = self.object
        return context


class ProfessionCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = ProfessionModel
    permission_required = 'admin_site.add_professionmodel'
    form_class = ProfessionForm
    template_name = 'admin_site/profession/index.html'
    success_message = 'Profession Successfully Registered'

    def get_success_url(self):
        return reverse('profession_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profession_list'] = ProfessionModel.objects.all().order_by('name')
        return context


class ProfessionListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ProfessionModel
    permission_required = 'admin_site.add_professionmodel'
    fields = '__all__'
    template_name = 'admin_site/profession/index.html'
    context_object_name = "profession_list"

    def get_queryset(self):
        return ProfessionModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProfessionForm
        return context


class ProfessionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ProfessionModel
    permission_required = 'admin_site.add_professionmodel'
    form_class = ProfessionForm
    template_name = 'admin_site/profession/index.html'
    success_message = 'Profession Successfully Updated'

    def get_success_url(self):
        return reverse('profession_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProfessionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = ProfessionModel
    permission_required = 'admin_site.add_professionmodel'
    fields = '__all__'
    template_name = 'admin_site/profession/delete.html'
    context_object_name = "profession"
    success_message = 'Profession Successfully Deleted'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('profession_index')


class CountryCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = CountryModel
    permission_required = 'admin_site.add_countrymodel'
    form_class = CountryForm
    template_name = 'admin_site/country/index.html'
    success_message = 'Country Successfully Registered'

    def get_success_url(self):
        return reverse('country_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['country_list'] = CountryModel.objects.all().order_by('name')
        return context


class CountryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = CountryModel
    permission_required = 'admin_site.add_countrymodel'
    fields = '__all__'
    template_name = 'admin_site/country/index.html'
    context_object_name = "country_list"

    def get_queryset(self):
        return CountryModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CountryForm
        return context


class CountryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CountryModel
    permission_required = 'admin_site.add_countrymodel'
    form_class = CountryForm
    template_name = 'admin_site/country/index.html'
    success_message = 'Country Successfully Updated'

    def get_success_url(self):
        return reverse('country_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CountryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = CountryModel
    permission_required = 'admin_site.add_countrymodel'
    fields = '__all__'
    template_name = 'admin_site/country/delete.html'
    context_object_name = "country"
    success_message = 'Country Successfully Deleted'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('country_index')
