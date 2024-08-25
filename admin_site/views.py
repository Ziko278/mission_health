import re

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin, messages
# from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.urls import reverse
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from communication.models import RecentActivityModel
from human_resource.forms import StaffProfileForm
from human_resource.models import StaffProfileModel, StaffModel
from student.models import StudentsModel, CohortModel
from admin_site.models import *
from admin_site.forms import *


class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'admin_site/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_activity_list'] = RecentActivityModel.objects.all().order_by('id').reverse()[:10]
        context['active_students'] = StudentsModel.objects.all().exclude(cohort__status=2).count()
        context['male_students'] = StudentsModel.objects.filter(gender='male').exclude(cohort__status=2).count()
        context['female_students'] = StudentsModel.objects.filter(gender='female').exclude(cohort__status=2).count()
        context['all_students'] = StudentsModel.objects.all().count()
        context['all_position'] = Group.objects.all().count()
        context['all_staff'] = StaffModel.objects.filter(status='active').count()
        context['cohort_list'] = CohortModel.objects.all().order_by('id').reverse()[:10]
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
        context['site_info'] = self.object
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
    permission_required = 'admin_site.change_siteinfomodel'
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
    permission_required = 'admin_site.view_siteinfomodel'
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
    permission_required = 'admin_site.change_siteinfomodel'
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
    permission_required = 'admin_site.change_siteinfomodel'
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
    permission_required = 'admin_site.change_siteinfomodel'
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
    permission_required = 'admin_site.view_siteinfomodel'
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
    permission_required = 'admin_site.change_siteinfomodel'
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
    permission_required = 'admin_site.change_siteinfomodel'
    fields = '__all__'
    template_name = 'admin_site/country/delete.html'
    context_object_name = "country"
    success_message = 'Country Successfully Deleted'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('country_index')


def admin_sign_in_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            intended_route = request.POST.get('next') or request.GET.get('next')
            remember_me = request.POST.get('remember_me') or request.GET.get('remember_me')

            if user.is_superuser:
                login(request, user)
                messages.success(request, 'welcome back {}'.format(user.username.title()))
                if remember_me:
                    request.session.set_expiry(3600 * 24 * 30)
                else:
                    request.session.set_expiry(0)
                if intended_route:
                    return redirect(intended_route)
                return redirect(reverse('admin_dashboard'))
            try:
                user_role = StaffProfileModel.objects.get(user=user)
            except StaffProfileModel.DoesNotExist:
                messages.error(request, 'Unknown Identity, Access Denied')
                return redirect(reverse('admin_login'))

            if user_role.staff:
                login(request, user)
                messages.success(request, 'welcome back {}'.format(user_role.staff))
                if remember_me:
                    request.session.set_expiry(3600 * 24 * 30)
                else:
                    request.session.set_expiry(0)
                if intended_route:
                    return redirect(intended_route)
                return redirect(reverse('admin_dashboard'))
            else:
                messages.error(request, 'Unknown Identity, Access Denied')
                return redirect(reverse('login'))
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect(reverse('admin_login'))

    return render(request, 'admin_site/sign_in.html')


def admin_sign_out_view(request):
    logout(request)
    return redirect(reverse('admin_login'))


class StaffProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'admin_site/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_superuser:
            staff = StaffProfileModel.objects.get(user=self.request.user).staff
            context['staff'] = staff
            context['form'] = StaffProfileForm(instance=staff)
        return context


class StaffProfileChangeView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = StaffModel
    template_name = 'admin_site/profile.html'
    form_class = StaffProfileForm
    success_message = 'Profile Successfully Updated'

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return redirect(reverse('site_info_edit', kwargs={'pk': 1}))
        return super(StaffProfileChangeView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('staff_profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff = StaffProfileModel.objects.get(user=self.request.user).staff
        context['staff'] = staff
        context['form'] = StaffProfileForm(instance=staff)
        return context


@login_required
def admin_change_password_view(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password1 = request.POST['new_password1']
        new_password2 = request.POST['new_password2']

        # Verify the current password
        if not request.user.check_password(current_password):
            messages.error(request, 'Incorrect current password.')
            return redirect(reverse('admin_change_password'))

        # Check if the new passwords match
        if len(new_password1) < 8:
            messages.error(request, 'Password must have at least 8 characters.')
            return redirect(reverse('admin_change_password'))

        if not re.match(r"^(?=.*[a-zA-Z])(?=.*\d).+$", new_password1):
            messages.error(request, 'Password must contain both letters and numbers.')
            return redirect(reverse('admin_change_password'))

        if new_password1 != new_password2:
            messages.error(request, 'New passwords do not match.')
            return redirect(reverse('admin_change_password'))

        # Update the user's password
        user = request.user
        user.set_password(new_password1)
        user.save()

        # Update the user's session with the new password
        update_session_auth_hash(request, user)

        logout(request)

        messages.success(request, 'Password successfully changed. Please log in with the new password.')
        return redirect('admin_login')

    return render(request, 'admin_site/change_password.html')