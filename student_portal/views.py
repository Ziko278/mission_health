import hashlib
import json
import re
import uuid

from cryptography.fernet import Fernet
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Sum, Q
from django.db.models.functions import Lower
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.template import RequestContext
import html
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied
from django.conf import settings
import requests
from django.core.exceptions import ValidationError
import hmac
from datetime import datetime, timedelta
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, JsonResponse, Http404
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from num2words import num2words

from admin_site.models import CountryModel, SiteInfoModel
from communication.forms import StudentMessageForm
from communication.models import CommunicationSettingModel, StudentMessageModel
from communication.views import account_activation_token, send_custom_email
from finance.models import FinanceSettingModel, TrainingPaymentModel, BankAccountModel, OnlinePaymentPlatformModel, \
    CurrencyModel
from student.forms import StudentForm, StudentProfileForm
from student.models import CohortModel, StudentProfileModel, StudentsModel
from student_portal.forms import SignUpForm, LoginForm
from training.forms import EnrollmentForm
from training.models import EnrollmentModel, CourseModel, LessonModel, LessonMaterialModel, ProgressModel, \
    LiveSessionModel
from django.contrib.sessions.models import Session
from django.utils import timezone


def log_out_other_sessions(request, user):
    # Get the current session key
    current_session_key = request.session.session_key

    # Get all sessions associated with this user
    sessions = Session.objects.filter(expire_date__gte=timezone.now())

    for session in sessions:
        data = session.get_decoded()
        if data.get('_auth_user_id') == str(user.id) and session.session_key != current_session_key:
            session.delete()  # Log out from other sessions


def student_signup_view(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()

            if student.id:
                request.session['registration_done'] = True
                return redirect(reverse('activation_mail', kwargs={'pk': student.pk}))
    else:
        form = StudentForm
    context = {
        'form': form,
        'country_list': CountryModel.objects.filter(status='active').order_by(Lower('name')),
        'cohort_list': CohortModel.objects.exclude(status='2')

    }
    return render(request, 'student_portal/register.html', context)


def send_activation_mail(request, pk):
    if not 'registration_done' in request.session:
        messages.error(request, 'Invalid Request')
        return redirect(reverse('homepage'))
    try:
        student = StudentsModel.objects.get(pk=pk)
    except Exception:
        return redirect(reverse('register_done'))
    try:
        user_profile = StudentProfileModel.objects.get(student=student)
        user = user_profile.user
        password = user_profile.default_password
    except Exception:
        return redirect(reverse('register_done'))

    communication_setting = CommunicationSettingModel.objects.first()
    if communication_setting:
        default_mail_account = communication_setting.default_smtp
        if default_mail_account:
            context = {
                'domain': get_current_site(request),
                'site_info': SiteInfoModel.objects.first(),
                'uid': urlsafe_base64_encode(str(user.pk).encode('utf-8')),
                'token': account_activation_token.make_token(user),
                'username': user.username,
                'password': password
            }
            mail_sent = send_custom_email(
                subject='Student Account Activation',
                recipient_list=[student.email],
                email_id=default_mail_account.id,
                template_name='student_portal/message/activation_mail_template.html',
                context=context
            )

            return redirect(reverse('register_done'))


def student_signup_done_view(request):
    if 'registration_done' in request.session:
        del request.session['registration_done']
        return render(request, 'student_portal/registration_done.html', {'registration_done': True})

    if 'activation_done' in request.session:
        del request.session['activation_done']
        return render(request, 'student_portal/registration_done.html', {'activation_done': True})

    return redirect('homepage')


#
def activate_account_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        request.session['activation_done'] = True
        return redirect('register_done')
    else:
        raise PermissionDenied()


def student_signin_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # try to log user by either username or password
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                try:
                    user = User.objects.get(email=username)
                except User.DoesNotExist:
                    user = None
            if not user:
                messages.error(request, 'Invalid Username or Email ')

            else: 
                 username = user.username 
                 user = authenticate(request, username=username, password=password) 
                 if user is not None:
                    try:
                        student = StudentProfileModel.objects.get(user=user).student
                    except Exception:
                        messages.error(request, 'Access Denied for current user')
                        return redirect(reverse('student_login'))

                    if user.is_active:
                        log_out_other_sessions(request, user)
                        if user.is_authenticated:
                            logout(request)
                        login(request, user)
                        messages.success(request, 'Welcome Back {}'.format(student.__str__()))
                        if 'remember_login' in request.POST:
                            request.session.set_expiry(0)
                            request.session.modified = True

                        nxt = request.GET.get("next", None)
                        if nxt:
                            return redirect(request.GET.get('next'))
                        return redirect(reverse('student_dashboard'))
                    else:
                        messages.error(request, 'Account not Activated')
                 else:
                    messages.error(request, 'Invalid Credentials')
        else:
            messages.error(request, 'Invalid Credentials')
    else:
        form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'student_portal/login.html', context)


def student_sign_out_view(request):
    logout(request)
    return redirect(reverse('student_login'))


class StudentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'student_portal/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = StudentProfileModel.objects.get(user=self.request.user).student
        context['student'] = student
        context['enrollment_list'] = EnrollmentModel.objects.filter(student=student, cohort=student.cohort)
        return context


class StudentProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'student_portal/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = StudentProfileModel.objects.get(user=self.request.user).student
        context['student'] = student
        context['form'] = StudentProfileForm(instance=student)
        return context


class StudentProfileChangeView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = StudentsModel
    template_name = 'student_portal/profile.html'
    form_class = StudentProfileForm
    success_message = 'Profile Successfully Updated'

    def get_success_url(self):
        return reverse('student_profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = StudentProfileModel.objects.get(user=self.request.user).student
        context['student'] = student
        context['form'] = StudentProfileForm(instance=student)
        return context


class StudentCourseDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'student_portal/course/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = StudentProfileModel.objects.get(user=self.request.user).student
        context['enrollment_list'] = EnrollmentModel.objects.filter(student=student, status='active')
        context['student'] = student
        return context


class StudentEnrollDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'student_portal/course/enroll_select.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = StudentProfileModel.objects.get(user=self.request.user).student
        context['course_list'] = CourseModel.objects.all()
        context['default_currency'] = FinanceSettingModel.objects.first().default_currency.symbol
        context['active_course_list'] = [enrollment.id for enrollment in EnrollmentModel.objects.filter(status='active', student=student)]
        context['student'] = student
        return context


class StudentEnrollmentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = EnrollmentModel
    form_class = EnrollmentForm
    template_name = 'student_portal/course/enroll.html'
    success_message = 'Course successfully Enrolled! Make payment to gain full access'

    def get_success_url(self):
        return reverse('student_enroll_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        student = StudentProfileModel.objects.get(user=self.request.user).student
        context['student'] = student
        context['course'] = get_object_or_404(CourseModel, pk=pk)
        context['default_currency'] = FinanceSettingModel.objects.first().default_currency.symbol

        return context


class StudentEnrollmentDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = EnrollmentModel
    template_name = 'student_portal/course/enroll_detail.html'
    context_object_name = 'enrollment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fee_paid'] = 0
        student = StudentProfileModel.objects.get(user=self.request.user).student
        context['student'] = student
        context['default_currency'] = FinanceSettingModel.objects.first().default_currency.symbol
        return context


class StudentLessonDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = LessonModel
    template_name = 'student_portal/course/lesson_detail.html'
    context_object_name = 'lesson'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = StudentProfileModel.objects.get(user=self.request.user).student
        context['student'] = student

        return context


class StudentLessonMaterialDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = LessonMaterialModel
    template_name = 'student_portal/course/lesson_material_detail.html'
    context_object_name = 'lesson_material'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = StudentProfileModel.objects.get(user=self.request.user).student
        context['student'] = student

        return context


class StudentFeeDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'student_portal/fee/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = StudentProfileModel.objects.get(user=self.request.user).student
        context['enrollment_list'] = EnrollmentModel.objects.filter(student=student, status='active')
        context['student'] = student
        context['default_currency'] = FinanceSettingModel.objects.first().default_currency.symbol

        return context


@login_required
def student_payment_amount(request, pk):
    enrollment = get_object_or_404(EnrollmentModel, pk=pk)
    student = StudentProfileModel.objects.get(user=request.user).student
    if enrollment.student != student:
        messages.error(request, 'Invalid Identity, Access Denied')
        referring_url = request.META.get('HTTP_REFERER')
        return redirect(referring_url)

    if request.method == 'POST':
        amount = request.POST.get('amount')
        request.session['amount'] = amount
        request.session['enrollmment_id'] = enrollment.id
        return redirect('select_payment_method')

    payments = TrainingPaymentModel.objects.filter(enrollment=enrollment, student=student, cohort=student.cohort,
                                                   status='confirmed')
    amount_paid = payments.aggregate(total_sum=Sum('amount_paid'))['total_sum']

    amount_paid = amount_paid if amount_paid else 0
    finance_setting = FinanceSettingModel.objects.first()
    minimum_payment = round(enrollment.amount * (finance_setting.minimum_payment/100))
    context = {
        'student': student,
        'enrollment': enrollment,
        'amount_paid': amount_paid,
        'balance': enrollment.amount - amount_paid,
        'default_currency': finance_setting.default_currency.symbol,
        'minimum_payment': minimum_payment
    }
    return render(request, 'student_portal/fee/payment_amount.html', context)


class StudentSelectPaymentMethodView(LoginRequiredMixin, TemplateView):
    template_name = 'student_portal/fee/select_method.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.session.get('amount') or not self.request.session.get('enrollmment_id'):
            messages.error(self.request, 'Invalid Request, Permission Denied')
            return redirect(reverse('student_dashboard'))
        return super(StudentSelectPaymentMethodView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = StudentProfileModel.objects.get(user=self.request.user).student
        enrollment_id = self.request.session.get('enrollmment_id')
        amount = self.request.session.get('amount')

        # del self.request.session['enrollmment_id']
        # del self.request.session['amount']
        global_offline_list = BankAccountModel.objects.filter(use_global=True)
        global_offline_id = [account.id for account in global_offline_list]
        other_offline_list = BankAccountModel.objects.filter(country=student.country).exclude(
            id__in=global_offline_id)

        global_online_list = OnlinePaymentPlatformModel.objects.filter(use_global=True)
        global_online_id = [account.id for account in global_online_list]
        other_online_list = OnlinePaymentPlatformModel.objects.filter(country=student.country).exclude(
            id__in=global_online_id)

        enrollment = get_object_or_404(EnrollmentModel, pk=enrollment_id)
        context['amount'] = amount
        context['amount_in_word'] = num2words(amount)
        context['enrollment'] = enrollment
        context['global_offline_list'] = global_offline_list
        context['other_offline_list'] = other_offline_list
        context['global_online_list'] = global_online_list
        context['other_online_list'] = other_online_list
        context['student'] = student
        context['default_currency'] = FinanceSettingModel.objects.first().default_currency

        return context


class PayWithPaystackView(LoginRequiredMixin, TemplateView):
    template_name = 'student_portal/fee/pay_with_paystack.html'

    def dispatch(self, *args, **kwargs):
        finance_setting = FinanceSettingModel.objects.first()
        try:
            amount = int(self.request.GET.get('amount'))
        except Exception:
            messages.error(self.request, 'An Error has occured, Try Later')
            return redirect(reverse('student_fee_dashboard'))

        return super(PayWithPaystackView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        finance_setting = FinanceSettingModel.objects.first()
        paystack = get_object_or_404(OnlinePaymentPlatformModel, pk=self.kwargs.get('paystack_pk'))
        key = paystack.key
        fernet = Fernet(key)
        student = StudentProfileModel.objects.get(user=self.request.user).student
        context['domain'] = get_current_site(self.request)
        amount = int(self.request.GET.get('amount'))
        context['default_currency'] = finance_setting.default_currency
        if finance_setting.default_currency != paystack.currency:
            amount *= paystack.currency.exchange_rate
            context['default_currency'] = paystack.currency
        context['amount'] = amount
        context['amount_in_word'] = num2words(context['amount'])

        context['enrollment'] = get_object_or_404(EnrollmentModel, pk=self.kwargs.get('pk'))
        context['paystack_secret_key'] = fernet.decrypt(paystack.public_key.encode()).decode()
        context['paystack_id'] = paystack.id
        context['email'] = student.email
        context['student'] = student
        context['callback_url'] = reverse('paystack_payment_done')

        return context


def verify_paystack_payment(reference, PAYSTACK_SECRET_KEY):
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    response = requests.get(url, headers=headers)
    return response.json()


def paystack_payment_done(request):
    reference = request.GET.get('reference')
    if not reference:
        context = {
            'status': 'error',
            'message': 'An Error has occurred or the payment was canceled'
        }
        return render(request, 'student_portal/fee/payment_done.html', context)

    paystack_id = request.GET.get('paystack_id')
    paystack = OnlinePaymentPlatformModel.objects.get(id=paystack_id)
    key = paystack.key
    fernet = Fernet(key)

    paystack_secret_key = fernet.decrypt(paystack.private_key.encode()).decode()

    # Verify payment
    result = verify_paystack_payment(reference, paystack_secret_key)

    if result['status'] and result['data']['status'] == 'success':
        try:
            student_id = result['data']['metadata']['custom_fields'][0]['value']
            enrollment_id = result['data']['metadata']['custom_fields'][1]['value']
            currency_id = result['data']['metadata']['custom_fields'][2]['value']

            student = StudentsModel.objects.get(id=student_id)
            enrollment = EnrollmentModel.objects.get(id=enrollment_id)
            currency = CurrencyModel.objects.get(id=currency_id)

            payment_exist = TrainingPaymentModel.objects.filter(platform_reference=reference)
            if payment_exist:
                messages.warning(request, 'A similar payment was found. Pls Contact Admin')
                return redirect(reverse('student_fee_dashboard'))

            value_in_currency = round(result['data']['amount'] / 100)
            finance_setting = FinanceSettingModel.objects.first()
            status = 'confirmed' if finance_setting.auto_confirm_online_payment else 'pending'
            if currency == finance_setting.default_currency:
                amount_paid = value_in_currency
            else:
                amount_paid = round(value_in_currency/currency.exchange_rate)

            payment = TrainingPaymentModel.objects.create(
                reference=reference,
                payment_method='online',
                student=student,
                enrollment=enrollment,
                status=status,
                value_in_currency=value_in_currency,
                currency=currency,
                default_currency=finance_setting.default_currency,
                amount_paid=amount_paid
            )

            payment.save()
            if payment.id:
                status = 'success'
                if finance_setting.auto_confirm_online_payment:
                    message = 'Payment Successful! We have received and confirmed your payment, Check Fee payment dashboard to print receipt'
                else:
                    message = 'Payment Successful! We have received your payment, We will confirm it in a moment, Pay attention to your fee dashboard'
            else:
                status = 'error'
                message = 'An Error has occurred or the payment was canceled, Please Contact Admin'

        except (StudentsModel.DoesNotExist, EnrollmentModel.DoesNotExist, CurrencyModel.DoesNotExist) as e:
            status = 'error'
            message = 'An Error has occurred or the payment was canceled, Please Contact Admin'

    else:
        status = 'error'
        message = 'An Error has occurred or the payment was canceled, Please Contact Admin'
    context = {
        'status': status,
        'message': message
    }
    return render(request, 'student_portal/fee/payment_done.html', context)


class PayWithPaypalView(TemplateView):
    template_name = 'student_portal/fee/pay_with_paypal.html'

    def dispatch(self, *args, **kwargs):
        finance_setting = FinanceSettingModel.objects.first()
        try:
            amount = int(self.request.GET.get('amount'))
        except Exception:
            messages.error(self.request, 'An Error has occurred, Try Later')
            return redirect(reverse('student_fee_dashboard'))

        return super(PayWithPaypalView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        finance_setting = FinanceSettingModel.objects.first()
        paypal = get_object_or_404(OnlinePaymentPlatformModel, pk=self.kwargs.get('paypal_pk'))
        key = paypal.key
        fernet = Fernet(key)
        student = StudentProfileModel.objects.get(user=self.request.user).student
        context['domain'] = get_current_site(self.request)
        amount = int(self.request.GET.get('amount'))
        context['default_currency'] = finance_setting.default_currency
        if finance_setting.default_currency != paypal.currency:
            amount *= paypal.currency.exchange_rate
            context['default_currency'] = paypal.currency
        context['amount'] = amount
        context['amount_in_word'] = num2words(context['amount'])

        context['enrollment'] = get_object_or_404(EnrollmentModel, pk=self.kwargs.get('pk'))
        context['paypal_client_id'] = fernet.decrypt(paypal.public_key.encode()).decode()
        context['paypal_id'] = paypal.id
        context['email'] = student.email
        context['student'] = student
        context['callback_url'] = reverse('paypal_payment_done')

        return context


def verify_paypal_payment(order_id, PAYPAL_ACCESS_TOKEN):
    url = f"https://sandbox.paypal.com/v2/checkout/orders/{order_id}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {PAYPAL_ACCESS_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    return response.json()


def paypal_payment_done(request):
    order_id = request.GET.get('paypal_order_id')
    if not order_id:
        context = {
            'status': 'error',
            'message': 'An Error has occurred or the payment was canceled'
        }
        return render(request, 'student_portal/fee/payment_done.html', context)

    paypal_id = request.GET.get('paypal_id')
    paypal = OnlinePaymentPlatformModel.objects.get(id=paypal_id)
    key = paypal.key
    fernet = Fernet(key)

    paypal_access_token = fernet.decrypt(paypal.private_key.encode()).decode()

    # Verify payment
    result = verify_paypal_payment(order_id, paypal_access_token)

    if result and result.get('status') == 'COMPLETED':

        try:
            custom_id = result['purchase_units'][0]['custom_id']
            student_id, enrollment_id, currency_id = custom_id.split(',')

            student = StudentsModel.objects.get(id=student_id)
            enrollment = EnrollmentModel.objects.get(id=enrollment_id)
            currency = CurrencyModel.objects.get(id=currency_id)

            payment_exist = TrainingPaymentModel.objects.filter(platform_reference=order_id)
            if payment_exist:
                messages.warning(request, 'A similar payment was found. Please Contact Admin')
                return redirect(reverse('student_fee_dashboard'))

            value_in_currency = float(result['purchase_units'][0]['amount']['value'])
            finance_setting = FinanceSettingModel.objects.first()
            status = 'confirmed' if finance_setting.auto_confirm_online_payment else 'pending'
            if currency == finance_setting.default_currency:
                amount_paid = value_in_currency
            else:
                amount_paid = round(value_in_currency / currency.exchange_rate)

            payment = TrainingPaymentModel.objects.create(
                reference=order_id,
                payment_method='online',
                student=student,
                enrollment=enrollment,
                status=status,
                value_in_currency=value_in_currency,
                currency=currency,
                default_currency=finance_setting.default_currency,
                amount_paid=amount_paid
            )

            payment.save()
            if payment.id:
                status = 'success'
                if finance_setting.auto_confirm_online_payment:
                    message = 'Payment Successful! We have received and confirmed your payment. Check Fee payment dashboard to print receipt'
                else:
                    message = 'Payment Successful! We have received your payment. We will confirm it in a moment. Pay attention to your fee dashboard'
            else:
                status = 'error'
                message = 'An Error has occurred or the payment was canceled. Please Contact Admin'

        except (StudentsModel.DoesNotExist, EnrollmentModel.DoesNotExist, CurrencyModel.DoesNotExist):
            status = 'error'
            message = 'An Error has occurred or the payment was canceled. Please Contact Admin'

    else:
        status = 'error'
        message = 'An Error has occurred or the payment was canceled. Please Contact Admin'
    context = {
        'status': status,
        'message': message
    }
    return render(request, 'student_portal/fee/payment_done.html', context)


class StudentPaymentListView(LoginRequiredMixin, ListView):
    model = TrainingPaymentModel
    template_name = 'student_portal/fee/payments.html'
    context_object_name = 'payment_list'

    def get_queryset(self):
        student = StudentProfileModel.objects.get(user=self.request.user).student
        return TrainingPaymentModel.objects.filter(cohort=student.cohort, student=student)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class StudentPaymentDetailView(DetailView):
    model = TrainingPaymentModel
    fields = '__all__'
    template_name = 'student_portal/fee/detail.html'
    context_object_name = "training_payment"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['amount_in_word'] = num2words(self.object.amount_paid)
        return context


@login_required
def student_change_password_view(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password1 = request.POST['new_password1']
        new_password2 = request.POST['new_password2']

        # Verify the current password
        if not request.user.check_password(current_password):
            messages.error(request, 'Incorrect current password.')
            return redirect(reverse('student_change_password'))

        # Check if the new passwords match
        if len(new_password1) < 8:
            messages.error(request, 'Password must have at least 8 characters.')
            return redirect(reverse('student_change_password'))

        if not re.match(r"^(?=.*[a-zA-Z])(?=.*\d).+$", new_password1):
            messages.error(request, 'Password must contain both letters and numbers.')
            return redirect(reverse('student_change_password'))

        if new_password1 != new_password2:
            messages.error(request, 'New passwords do not match.')
            return redirect(reverse('student_change_password'))

        # Update the user's password
        user = request.user
        user.set_password(new_password1)
        user.save()

        # Update the user's session with the new password
        update_session_auth_hash(request, user)

        logout(request)

        messages.success(request, 'Password successfully changed. Please log in with the new password.')
        return redirect('student_login')

    return render(request, 'student_portal/change_password.html')


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_user = User.objects.filter(email=data).first()
            if associated_user:
                subject = "Password Reset Requested"
                email_template_name = "password_reset_email.html"
                context = {
                    "email": associated_user.email,
                    'domain': get_current_site(request).domain,
                    'site_name': 'Your site',
                    "uid": urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    "user": associated_user,
                    'token': default_token_generator.make_token(associated_user),
                    'protocol': 'http',
                }
                email = render_to_string(email_template_name, context)
                try:
                    send_mail(subject, email, 'your-email@gmail.com', [associated_user.email], fail_silently=False)
                except BadHeaderError:
                    messages.error(request, 'An Error has Occured, Try Later')
                    return redirect("password_reset")
                return redirect("password_reset_done")
    password_reset_form = PasswordResetForm()
    return render(request, "student_portal/password_reset.html", {"password_reset_form": password_reset_form})


def password_reset_confirm(request, uidb64=None, token=None):
    logout(request)
    if request.method == 'POST':
        form = SetPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('password_reset_complete')
    else:
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            form = SetPasswordForm(user=user)
        else:
            return HttpResponse('Password reset link is invalid.')

    return render(request, 'password_reset_confirm.html', {'form': form})


@login_required
def mark_lesson_material_completed(request, pk):
    if request.method == 'POST':
        material = get_object_or_404(LessonMaterialModel, pk=pk)
        lesson = material.lesson
        student = StudentProfileModel.objects.get(user=request.user).student
        progress = ProgressModel.objects.filter(student=student, cohort=student.cohort).first()
        if not progress:
            progress = ProgressModel.objects.create(student=student, cohort=student.cohort, progress={})
            progress.save()
        progress_data = progress.progress
        if str(lesson.id) in progress_data:
            if material.id not in progress_data[str(lesson.id)]:
                progress_data[str(lesson.id)].append(material.id)
        else:
            progress_data[str(lesson.id)] = [material.id]
        progress.save()
        messages.success(request, 'Material marked as completed')
        return redirect(request.META.get('HTTP_REFERER', reverse('student_lesson_detail', kwargs={'pk': lesson.id})))
    messages.error(request, 'Invalid Request')
    return redirect(request.META.get('HTTP_REFERER', reverse('student_dashboard')))


class StudentMessageCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = StudentMessageModel
    form_class = StudentMessageForm
    success_message = 'Message Sent! We will get back to you soon'
    template_name = 'student_portal/message/create.html'

    def get_success_url(self):
        return reverse('student_message_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class StudentMessageListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = StudentMessageModel
    template_name = 'student_portal/message/index.html'
    context_object_name = "message_list"

    def get_queryset(self):
        student = StudentProfileModel.objects.get(user=self.request.user).student
        return StudentMessageModel.objects.filter(Q(from_student=student) | Q(to_student=student)).order_by('created_at').reverse()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class StudentMessageDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = StudentMessageModel
    template_name = 'student_portal/message/detail.html'
    context_object_name = "message"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class StudentLiveClassView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = LiveSessionModel
    template_name = 'student_portal/course/live_class.html'
    context_object_name = "live_class_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


