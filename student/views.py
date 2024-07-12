from django.db.models.functions import Lower
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
from finance.models import FinanceSettingModel
from student.models import StudentsModel
from student.models import *
from student.forms import *
from training.models import EnrollmentModel


class CohortCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = CohortModel
    permission_required = 'student.add_cohortmodel'
    form_class = CohortForm
    template_name = 'student/cohort/index.html'
    success_message = 'Cohort Successfully Registered'

    def get_success_url(self):
        return reverse('cohort_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cohort_list'] = CohortModel.objects.all().order_by('name')
        return context


class CohortListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = CohortModel
    permission_required = 'student.view_cohortmodel'
    fields = '__all__'
    template_name = 'student/cohort/index.html'
    context_object_name = "cohort_list"

    def get_queryset(self):
        return CohortModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CohortForm
        return context


class CohortUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CohortModel
    permission_required = 'student.change_cohortmodel'
    form_class = CohortForm
    template_name = 'student/cohort/index.html'
    success_message = 'Cohort Successfully Updated'

    def get_success_url(self):
        return reverse('cohort_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CohortDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = CohortModel
    permission_required = 'student.view_cohortmodel'
    template_name = 'student/cohort/detail.html'
    context_object_name = 'cohort'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student_list'] = StudentsModel.objects.filter(cohort=self.object)
        return context


class CohortDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = CohortModel
    permission_required = 'student.delete_cohortmodel'
    fields = '__all__'
    template_name = 'student/cohort/delete.html'
    context_object_name = "cohort"
    success_message = 'Cohort Successfully Deleted'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('cohort_index')


class StudentCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = StudentsModel
    permission_required = 'student.add_studentsmodel'
    form_class = StudentForm
    template_name = 'student/student/create.html'
    success_message = 'Student Successfully Registered'

    def get_success_url(self):
        return reverse('student_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cohort_list'] = CohortModel.objects.exclude(status='2')
        context['country_list'] = CountryModel.objects.filter(status='active').order_by(Lower('name'))

        return context


class StudentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = StudentsModel
    permission_required = 'student.view_studentsmodel'
    fields = '__all__'
    template_name = 'student/student/index.html'
    context_object_name = "student_list"

    def get_queryset(self):
        return StudentsModel.objects.filter().exclude(cohort__status=2).order_by('surname')


class StudentAlumniListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = StudentsModel
    permission_required = 'student.view_studentsmodel'
    fields = '__all__'
    template_name = 'student/student/alumni.html'
    context_object_name = "student_list"

    def get_queryset(self):
        return StudentsModel.objects.filter().filter(status='graduated').order_by('surname')


class StudentDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = StudentsModel
    permission_required = 'student.view_studentsmodel'
    fields = '__all__'
    template_name = 'student/student/detail.html'
    context_object_name = "student"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enrollment_list'] = EnrollmentModel.objects.filter(student=self.object, status='active')
        context['default_currency'] = FinanceSettingModel.objects.first().default_currency.symbol
        return context


class StudentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = StudentsModel
    permission_required = 'student.change_studentsmodel'
    form_class = StudentForm
    template_name = 'student/student/edit.html'
    success_message = 'Student Information Successfully Updated'

    def get_success_url(self):
        return reverse('student_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student'] = self.object
        context['student_setting'] = StudentSettingModel.objects.filter().first()
        context['cohort_list'] = CohortModel.objects.exclude(status='2')
        context['country_list'] = CountryModel.objects.filter(status='active').order_by(Lower('name'))

        return context


class StudentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = StudentsModel
    permission_required = 'student.delete_studentsmodel'
    fields = '__all__'
    template_name = 'student/student/delete.html'
    context_object_name = "student"
    success_message = 'Student Successfully Deleted'

    def get_success_url(self):
        return reverse('student_index')

