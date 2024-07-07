from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import EmailMessage, send_mail, get_connection, EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from num2words import num2words
from six import text_type

from communication.models import *
from communication.forms import *

from django.core.mail import send_mail, EmailMessage
from django.core.mail.backends.smtp import EmailBackend

from django.core.mail import EmailMessage, get_connection
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_custom_email(subject, recipient_list, email_id, template_name, context):
    try:
        email_setting = SMTPConfigurationModel.objects.get(pk=email_id)
    except SMTPConfigurationModel.DoesNotExist:
        raise ValueError("No email setting found")

    # Set up email backend
    email_backend = get_connection(
        host=email_setting.host,
        port=email_setting.port,
        username=email_setting.email,
        password=email_setting.password,
        use_tls=email_setting.use_tls,
    )

    # Render HTML content from template
    html_content = render_to_string(template_name, context)

    # Create plain text version by stripping HTML tags
    plain_content = strip_tags(html_content)

    # Create email message with alternatives (HTML and plain text)
    email = EmailMultiAlternatives(
        subject=subject,
        body=plain_content,
        from_email=email_setting.email,
        to=recipient_list,
        connection=email_backend
    )
    email.attach_alternative(html_content, "text/html")

    # Send the email
    try:
        mail_sent = email.send()
    except Exception as e:
        mail_sent = False
        # Handle exceptions or logging here
        print(f"Failed to send email: {str(e)}")

    return mail_sent




# Example usage
# send_custom_email(
#     subject='Test Email',
#     message='This is a test email.',
#     recipient_list=['recipient@example.com'],
#     email_setting_name='Gmail Account'
# )


class SMTPConfigurationCreateView(SuccessMessageMixin, CreateView):
    model = SMTPConfigurationModel
    form_class = SMTPConfigurationForm
    success_message = 'Email Configuration Added Successfully'
    template_name = 'communication/smtp_configuration/index.html'

    def get_success_url(self):
        return reverse('smtp_configuration_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['smtp_configuration_list'] = SMTPConfigurationModel.objects.all().order_by('name')
        return context


class SMTPConfigurationListView(ListView):
    model = SMTPConfigurationModel
    fields = '__all__'
    template_name = 'communication/smtp_configuration/index.html'
    context_object_name = "smtp_configuration_list"

    def get_queryset(self):
        return SMTPConfigurationModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SMTPConfigurationForm
        context['staff_list'] = StaffModel.objects.all()

        return context


class SMTPConfigurationUpdateView(SuccessMessageMixin, UpdateView):
    model = SMTPConfigurationModel
    form_class = SMTPConfigurationForm
    success_message = 'Email Configuration Updated Successfully'
    template_name = 'communication/smtp_configuration/index.html'

    def get_success_url(self):
        return reverse('smtp_configuration_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['smtp_configuration_list'] = SMTPConfigurationModel.objects.all().order_by('name')

        return context


class SMTPConfigurationDeleteView(SuccessMessageMixin, DeleteView):
    model = SMTPConfigurationModel
    success_message = 'Email Configuration Deleted Successfully'
    fields = '__all__'
    template_name = 'communication/smtp_configuration/delete.html'
    context_object_name = "smtp_configuration"

    def get_success_url(self):
        return reverse("smtp_configuration_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MessageCreateView(SuccessMessageMixin, CreateView):
    model = MessageModel
    form_class = MessageForm
    success_message = 'Message Saved Successfully'
    template_name = 'communication/message/index.html'

    def get_success_url(self):
        return reverse('message_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message_list'] = MessageModel.objects.filter(user=self.request.user).order_by('created_at').reverse()
        return context


class MessageListView(ListView):
    model = MessageModel
    fields = '__all__'
    template_name = 'communication/message/index.html'
    context_object_name = "message_list"

    def get_queryset(self):
        return MessageModel.objects.filter(user=self.request.user).order_by('created_at').reverse()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MessageForm

        return context


class MessageUpdateView(SuccessMessageMixin, UpdateView):
    model = MessageModel
    form_class = MessageForm
    success_message = 'Message Updated Successfully'
    template_name = 'communication/message/index.html'

    def get_success_url(self):
        return reverse('message_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message_list'] = MessageModel.objects.filter(user=self.request.user).order_by('created_at').reverse()

        return context


class MessageDeleteView(SuccessMessageMixin, DeleteView):
    model = MessageModel
    success_message = 'Message Deleted Successfully'
    fields = '__all__'
    template_name = 'communication/message/delete.html'
    context_object_name = "message"

    def get_success_url(self):
        return reverse("message_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def check_mail_setup(request):
    communication_setting = CommunicationSettingModel.objects.first()
    if not communication_setting:
        messages.error(request, 'Communication Setting Not Found, Try Later')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    if not communication_setting.default_smtp:
        messages.error(request, 'Email Setting Not Found, Try Later')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    smtp_config = communication_setting.default_smtp
    smtp_connection = get_connection(
        host=smtp_config.host,
        port=smtp_config.port,
        username=smtp_config.username,
        password=smtp_config.password,
        use_tls=True,  # Adjust based on your SMTP configuration
    )
    return smtp_connection, smtp_config.email


class CommunicationSettingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = CommunicationSettingModel
    form_class = CommunicationSettingForm
    permission_required = 'communication.change_communicationsettingmodel'
    success_message = 'Communication Setting Updated Successfully'
    template_name = 'communication/setting/create.html'

    def dispatch(self, *args, **kwargs):
        communication_setting = CommunicationSettingModel.objects.first()
        if not communication_setting:
            return super(CommunicationSettingCreateView, self).dispatch(*args, **kwargs)
        else:
            return redirect(reverse('communication_setting_edit', kwargs={'pk': communication_setting.pk}))

    def get_success_url(self):
        return reverse('communication_setting_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CommunicationSettingDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = CommunicationSettingModel
    permission_required = 'communication.view_communicationsettingmodel'
    fields = '__all__'
    template_name = 'communication/setting/detail.html'
    context_object_name = "communication_setting"

    def dispatch(self, *args, **kwargs):
        communication_setting = CommunicationSettingModel.objects.first()
        if communication_setting:
            if self.kwargs.get('pk') != communication_setting.id:
                return redirect(reverse('communication_setting_detail', kwargs={'pk': communication_setting.pk}))
            return super(CommunicationSettingDetailView, self).dispatch(*args, **kwargs)
        else:
            return redirect(reverse('communication_setting_create'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class CommunicationSettingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CommunicationSettingModel
    permission_required = 'communication.change_communicationsettingmodel'
    form_class = CommunicationSettingForm
    success_message = 'Communication Setting Updated Successfully'
    template_name = 'communication/setting/create.html'

    def get_success_url(self):
        return reverse('communication_setting_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['communication_setting'] = self.object
        return context


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.pk) + text_type(timestamp) + text_type(user.is_active)


account_activation_token = TokenGenerator()


# def send_activation_mail(request, user, to_email):
#     context = {
#         'domain': get_current_site(request),
#         'uid': urlsafe_base64_encode(str(user.pk).encode('utf-8')),
#         'token': account_activation_token.make_token(user)
#     }
#
#     mail_subject = 'U2ME Account Activation'
#     from_email = settings.EMAIL_HOST_USER
#     html_message = render_to_string('communication/account/verify_account.html', context)
#     plain_message = strip_tags(html_message)
#
#     mail_sent = send_mail(mail_subject, plain_message, from_email, [to_email], html_message=html_message,
#                           fail_silently=True)
#     return mail_sent


def send_test_email_view(request):
    send_custom_email(
        subject='Test Email',
        message='This is a test email sent from a dynamic email setting.',
        recipient_list=['recipient@example.com'],
        email_setting_name='Gmail Account'
    )
    return HttpResponse("Test email sent successfully.")