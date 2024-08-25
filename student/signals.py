from django.contrib.sites.shortcuts import get_current_site
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.http import urlsafe_base64_encode

from communication.views import account_activation_token, send_custom_email
from student.models import *
from django.contrib.auth.models import User
from communication.models import RecentActivityModel, CommunicationSettingModel
from training.models import ProgressModel


@receiver(post_save, sender=StudentsModel)
def create_student_account(sender, instance, created, **kwargs):
    if created:
        student = instance

        username = student.registration_number
        password = User.objects.make_random_password(length=8)
        email = student.email

        user = User.objects.create_user(username=username, email=email, password=password)
        if not student.user:
            user.is_active = False
            user.save()
        user_profile = StudentProfileModel.objects.create(user=user, student=student, default_password=password)
        user_profile.save()

        student.save()

        id_generator = StudentIDGeneratorModel.objects.filter(last_student_id=student.registration_number).last()
        id_generator.status = 's'
        id_generator.save()

        category = 'student_registration'
        subject = "<b>{}</b> just completed student registration".format(instance.__str__().title(), )
        activity = RecentActivityModel.objects.create(category=category, subject=subject, reference_id=instance.id)
        activity.save()

        progress = ProgressModel.objects.create(student=student, cohort=student.cohort)
        progress.save()

