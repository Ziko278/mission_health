from django.db import models
from django.contrib.auth.models import User
from human_resource.models import StaffModel
from student.models import StudentsModel


class RecentActivityModel(models.Model):
    category = models.CharField(max_length=100)
    subject = models.CharField(max_length=250)
    reference_id = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


class SMTPConfigurationModel(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    host = models.CharField(max_length=200)
    port = models.PositiveIntegerField()
    use_tls = models.BooleanField(default=True)
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    staff = models.ForeignKey(StaffModel, on_delete=models.CASCADE, blank=True, null=True)
    is_general = models.BooleanField(default=False)

    def __str__(self):
        return self.name.upper()


class CommunicationSettingModel(models.Model):
    default_smtp = models.ForeignKey(SMTPConfigurationModel, on_delete=models.SET_NULL, null=True, blank=True)
    auto_save_sent_message = models.BooleanField(default=False)


class MessageModel(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.title.upper()


class StudentMessageModel(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    from_student = models.ForeignKey(StudentsModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='from_student')
    to_student = models.ForeignKey(StudentsModel, on_delete=models.SET_NULL, null=True, blank=True)
    is_replied = models.BooleanField(blank=True, default=False)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.title.upper()

