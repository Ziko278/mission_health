from django.core import serializers
from django.db.models.functions import Lower
from django.http import HttpResponse
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
from num2words import num2words

from communication.models import RecentActivityModel
from finance.models import *
from finance.forms import *


class CurrencyCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = CurrencyModel
    permission_required = 'finance.change_financesettingmodel'
    form_class = CurrencyForm
    template_name = 'finance/currency/index.html'
    success_message = 'Currency Successfully Registered'

    def get_success_url(self):
        return reverse('currency_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['currency_list'] = CurrencyModel.objects.all().order_by('name')
        return context


class CurrencyListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = CurrencyModel
    permission_required = 'finance.view_financesettingmodel'
    fields = '__all__'
    template_name = 'finance/currency/index.html'
    context_object_name = "currency_list"

    def get_queryset(self):
        return CurrencyModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CurrencyForm
        context['country_list'] = CountryModel.objects.filter(status='active').order_by(Lower('name'))
        return context


class CurrencyUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CurrencyModel
    permission_required = 'finance.change_financesettingmodel'
    form_class = CurrencyForm
    template_name = 'finance/currency/index.html'
    success_message = 'Currency Successfully Updated'

    def get_success_url(self):
        return reverse('currency_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CurrencyDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = CurrencyModel
    permission_required = 'finance.change_financesettingmodel'
    fields = '__all__'
    template_name = 'finance/currency/delete.html'
    context_object_name = "currency"
    success_message = 'Currency Successfully Deleted'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('currency_index')


class FinanceSettingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = FinanceSettingModel
    form_class = FinanceSettingForm
    permission_required = 'finance.change_financesettingmodel'
    success_message = 'Finance Setting Updated Successfully'
    template_name = 'finance/setting/create.html'

    def dispatch(self, *args, **kwargs):
        finance_setting = FinanceSettingModel.objects.first()
        if not finance_setting:
            return super(FinanceSettingCreateView, self).dispatch(*args, **kwargs)
        else:
            return redirect(reverse('finance_setting_edit', kwargs={'pk': finance_setting.pk}))

    def get_success_url(self):
        return reverse('finance_setting_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class FinanceSettingDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = FinanceSettingModel
    permission_required = 'finance.view_financesettingmodel'
    fields = '__all__'
    template_name = 'finance/setting/detail.html'
    context_object_name = "finance_setting"

    def dispatch(self, *args, **kwargs):
        finance_setting = FinanceSettingModel.objects.first()
        if finance_setting:
            if self.kwargs.get('pk') != finance_setting.id:
                return redirect(reverse('finance_setting_detail', kwargs={'pk': finance_setting.pk}))
            return super(FinanceSettingDetailView, self).dispatch(*args, **kwargs)
        else:
            return redirect(reverse('finance_setting_create'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class FinanceSettingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = FinanceSettingModel
    permission_required = 'finance.change_financesettingmodel'
    form_class = FinanceSettingForm
    success_message = 'Finance Setting Updated Successfully'
    template_name = 'finance/setting/create.html'

    def get_success_url(self):
        return reverse('finance_setting_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['finance_setting'] = self.object
        return context


class BankAccountCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = BankAccountModel
    permission_required = 'finance.change_financesettingmodel'
    form_class = BankAccountForm
    template_name = 'finance/bank_account/index.html'
    success_message = 'Bank Account Successfully Registered'

    def get_success_url(self):
        return reverse('bank_account_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bank_account_list'] = BankAccountModel.objects.all()
        return context


class BankAccountListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = BankAccountModel
    permission_required = 'finance.view_financesettingmodel'
    fields = '__all__'
    template_name = 'finance/bank_account/index.html'
    context_object_name = "bank_account_list"

    def get_queryset(self):
        return BankAccountModel.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BankAccountForm
        context['country_list'] = CountryModel.objects.filter(status='active').order_by(Lower('name'))
        context['currency_list'] = CurrencyModel.objects.filter(status='active').order_by(Lower('name'))
        return context


class BankAccountUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = BankAccountModel
    permission_required = 'finance.change_financesettingmodel'
    form_class = BankAccountForm
    template_name = 'finance/bank_account/index.html'
    success_message = 'Bank Account Successfully Updated'

    def get_success_url(self):
        return reverse('bank_account_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BankAccountDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = BankAccountModel
    permission_required = 'finance.change_financesettingmodel'
    fields = '__all__'
    template_name = 'finance/bank_account/delete.html'
    context_object_name = "bank_account"
    success_message = 'Bank Account Successfully Deleted'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('bank_account_index')


class OnlinePaymentPlatformCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = OnlinePaymentPlatformModel
    permission_required = 'finance.change_financesettingmodel'
    form_class = OnlinePaymentPlatformForm
    success_message = 'Payment Method Added Successfully'
    template_name = 'finance/online_payment/index.html'

    def get_success_url(self):
        return reverse('online_payment_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['online_payment_list'] = OnlinePaymentPlatformModel.objects.all().order_by('name')

        return context


class OnlinePaymentPlatformListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = OnlinePaymentPlatformModel
    permission_required = 'finance.view_financesettingmodel'
    fields = '__all__'
    template_name = 'finance/online_payment/index.html'
    context_object_name = "online_payment_list"

    def get_queryset(self):
        return OnlinePaymentPlatformModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OnlinePaymentPlatformForm

        return context


class OnlinePaymentPlatformDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = OnlinePaymentPlatformModel
    permission_required = 'finance.view_financesettingmodel'
    fields = '__all__'
    template_name = 'finance/online_payment/detail.html'
    context_object_name = "method"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        key = self.object.key
        fernet = Fernet(key)
        context['public_key'] = fernet.decrypt(self.object.public_key.encode()).decode()
        context['private_key'] = fernet.decrypt(self.object.private_key.encode()).decode()
        context['form'] = OnlinePaymentPlatformForm(instance=self.object)
        return context


class OnlinePaymentPlatformUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = OnlinePaymentPlatformModel
    permission_required = 'finance.change_financesettingmodel'
    form_class = OnlinePaymentPlatformForm
    success_message = 'Online Payment Method Updated Successfully'
    template_name = 'finance/online_payment/index.html'

    def get_success_url(self):
        return reverse('online_payment_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['online_payment_list'] = OnlinePaymentPlatformModel.objects.all().order_by('name')

        return context


class OnlinePaymentPlatformDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = OnlinePaymentPlatformModel
    permission_required = 'finance.change_financesettingmodel'
    success_message = 'Online Payment Method Deleted Successfully'
    fields = '__all__'
    template_name = 'finance/online_payment/delete.html'
    context_object_name = "online_payment"

    def get_success_url(self):
        return reverse("online_payment_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TrainingPaymentCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = TrainingPaymentModel
    permission_required = 'finance.add_trainingpaymentmodel'
    form_class = TrainingPaymentForm
    success_message = 'Training Payment Successful'
    template_name = 'finance/training_payment/create.html'

    def get_success_url(self):
        return reverse('training_payment_create', kwargs={'student_pk': self.object.student.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = StudentsModel.objects.get(pk=self.kwargs.get('student_pk'))
        context['student'] = student
        context['course_list'] = CourseModel.objects.all().order_by('name')
        context['payment_list'] = TrainingPaymentModel.objects.filter(student__id=student.id, cohort=student.cohort)
        return context


class TrainingPaymentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = TrainingPaymentModel
    permission_required = 'finance.view_trainingpaymentmodel'
    fields = '__all__'
    template_name = 'finance/training_payment/index.html'
    context_object_name = "training_payment_list"

    def get_queryset(self):
        return TrainingPaymentModel.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['training_payment_list'] = TrainingPaymentModel.objects.all()
        context['cohort_list'] = CohortModel.objects.all()
        context['form'] = TrainingPaymentForm

        return context


class TrainingPaymentDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = TrainingPaymentModel
    permission_required = 'finance.view_trainingpaymentmodel'
    fields = '__all__'
    template_name = 'finance/training_payment/detail.html'
    context_object_name = "training_payment"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['amount_in_word'] = num2words(self.object.amount_paid)
        return context


class TrainingPaymentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = TrainingPaymentModel
    permission_required = 'finance.change_trainingpaymentmodel'
    form_class = TrainingPaymentEditForm
    success_message = 'Training Payment Updated Successfully'
    template_name = 'finance/training_payment/index.html'

    def get_success_url(self):
        return reverse('training_payment_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['training_payment_list'] = TrainingPaymentModel.objects.all()

        return context


class TrainingPaymentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = TrainingPaymentModel
    permission_required = 'finance.delete_trainingpaymentmodel'
    success_message = 'Training Payment Deleted Successfully'
    fields = '__all__'
    template_name = 'finance/training_payment/delete.html'
    context_object_name = "training_payment"

    def get_success_url(self):
        return reverse("training_payment_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TrainingPaymentSelectStudentView(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin, TemplateView):
    template_name = 'finance/training_payment/select_student.html'
    permission_required = 'finance.add_trainingpaymentmodel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_list = StudentsModel.objects.all()
        context['student_list'] = serializers.serialize("json", student_list)
        return context


def fee_get_class_students_by_reg_number(request):
    reg_no = request.GET.get('reg_no')

    student_list = StudentsModel.objects.filter(registration_number__icontains=reg_no)
    result = ''
    for student in student_list:
        full_name = student.__str__()
        result += """<li class='list-group-item select_student d-flex justify-content-between align-items-center' student_id={}>
        {} </li>""".format(student.id, full_name)
    if result == '':
        result += """<li class='list-group-item d-flex justify-content-between align-items-center bg-danger text-white'>
        No Student in with inputted Registration Number</li>"""
    return HttpResponse(result)
