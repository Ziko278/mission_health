from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from student.models import *
from django.contrib.auth.models import User
from communication.models import RecentActivityModel


@receiver(post_save, sender=StudentsModel)
def create_student_account(sender, instance, created, **kwargs):
    if created:
        student = instance

        username = student.registration_number
        password = User.objects.make_random_password(length=8)
        email = student.email

        user = User.objects.create_user(username=username, email=email, password=password)
        user_profile = StudentProfileModel.objects.create(user=user, student=student, default_password=password)
        user_profile.save()

        student.save()

        id_generator = StudentIDGeneratorModel.objects.filter(last_student_id=student.registration_number).last()
        id_generator.status = 's'
        id_generator.save()


@receiver(post_save, sender=StudentsModel)
def create_registration_notification(sender, instance, created, **kwargs):
    if created:
        category = 'student_registration'
        subject = "<b>{}</b> just completed student registration".format(instance.__str__().title(),)
        activity = RecentActivityModel.objects.create(category=category, subject=subject, reference_id=instance.id)
        activity.save()
