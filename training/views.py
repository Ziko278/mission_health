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
from training.models import *
from training.forms import *


class CourseCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = CourseModel
    permission_required = 'training.add_coursemodel'
    form_class = CourseForm
    template_name = 'training/course/index.html'
    success_message = 'Course Successfully Registered'

    def get_success_url(self):
        return reverse('course_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course_list'] = CourseModel.objects.all().order_by('name')
        return context


class CourseListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = CourseModel
    permission_required = 'training.add_coursemodel'
    fields = '__all__'
    template_name = 'training/course/index.html'
    context_object_name = "course_list"

    def get_queryset(self):
        return CourseModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CourseForm
        return context


class CourseUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CourseModel
    permission_required = 'training.add_coursemodel'
    form_class = CourseForm
    template_name = 'training/course/index.html'
    success_message = 'Course Successfully Updated'

    def get_success_url(self):
        return reverse('course_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CourseDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = CourseModel
    permission_required = 'training.add_coursemodel'
    fields = '__all__'
    template_name = 'training/course/delete.html'
    context_object_name = "course"
    success_message = 'Course Successfully Deleted'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('course_index')


class LessonCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = LessonModel
    permission_required = 'training.add_lessonmodel'
    form_class = LessonForm
    template_name = 'training/lesson/create.html'
    success_message = 'Lesson Successfully Added'

    def get_success_url(self):
        return reverse('lesson_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course_list'] = CourseModel.objects.all().order_by('name')

        return context


class LessonListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = LessonModel
    permission_required = 'training.view_lessonmodel'
    fields = '__all__'
    template_name = 'training/lesson/index.html'
    context_object_name = "lesson_list"

    def get_queryset(self):
        return LessonModel.objects.all().order_by('course__name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = LessonForm
        context['course_list'] = CourseModel.objects.all().order_by('name')

        return context


class LessonDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = LessonModel
    permission_required = 'training.view_lessonmodel'
    fields = '__all__'
    template_name = 'training/lesson/detail.html'
    context_object_name = "lesson"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['material_list'] = LessonMaterialModel.objects.filter(lesson=self.object).order_by('order')
        return context


class LessonUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = LessonModel
    permission_required = 'training.change_lessonmodel'
    form_class = LessonForm
    template_name = 'training/lesson/edit.html'
    success_message = 'Lesson Successfully Updated'

    def get_success_url(self):
        return reverse('lesson_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LessonDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = LessonModel
    permission_required = 'training.delete_lessonmodel'
    fields = '__all__'
    template_name = 'training/lesson/delete.html'
    context_object_name = "lesson"
    success_message = 'Lesson Successfully Deleted'

    def get_success_url(self):
        return reverse('lesson_index')


class LessonMaterialCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = LessonMaterialModel
    permission_required = 'training.add_lessonmaterialmodel'
    form_class = LessonMaterialForm
    template_name = 'training/lesson_material/create.html'
    success_message = 'Lesson Material Successfully Added'

    def get_success_url(self):
        return reverse('lesson_material_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lesson_id'] = self.kwargs.get('pk')
        return context


class LessonMaterialNoteCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = LessonMaterialModel
    permission_required = 'training.add_lessonmaterialmodel'
    form_class = LessonMaterialForm
    template_name = 'training/lesson_material/create_note.html'
    success_message = 'Lesson Material Successfully Added'

    def get_success_url(self):
        return reverse('lesson_detail', kwargs={'pk': self.object.lesson.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lesson_id'] = self.kwargs.get('pk')
        return context


class LessonMaterialListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = LessonMaterialModel
    permission_required = 'training.view_lessonmaterialmodel'
    fields = '__all__'
    template_name = 'training/lesson_material/index.html'
    context_object_name = "lesson_material_list"

    def get_queryset(self):
        return LessonMaterialModel.objects.all().order_by('lesson__course__name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LessonMaterialDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = LessonMaterialModel
    permission_required = 'training.view_lessonmaterialmodel'
    fields = '__all__'
    template_name = 'training/lesson_material/detail.html'
    context_object_name = "lesson_material"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LessonMaterialUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = LessonMaterialModel
    permission_required = 'training.change_lessonmaterialmodel'
    form_class = LessonMaterialForm
    template_name = 'training/lesson_material/edit.html'
    success_message = 'Lesson Material Successfully Updated'

    def get_success_url(self):
        return reverse('lesson_material_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LessonMaterialDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = LessonMaterialModel
    permission_required = 'training.delete_lessonmaterialmodel'
    fields = '__all__'
    template_name = 'training/lesson_material/delete.html'
    context_object_name = "lesson_material"
    success_message = 'Lesson Material Successfully Deleted'

    def get_success_url(self):
        return reverse('lesson_material_index')

