from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from communication.models import RecentActivityModel
from human_resource.models import StaffModel, StaffIDGeneratorModel, StaffProfileModel
from django.contrib.auth.models import User


@receiver(post_save, sender=StaffModel)
def create_staff_account(sender, instance, created, **kwargs):
    if created:
        staff = instance
        username = staff.staff_id
        password = User.objects.make_random_password(length=8)
        email = staff.email

        user = User.objects.create_user(username=username, email=email, password=password, is_active=True, is_staff=True)
        user_profile = StaffProfileModel.objects.create(user=user, staff=staff,
                                                       default_password=password)
        user_profile.save()

        staff.group.user_set.add(user)

        id_generator = StaffIDGeneratorModel.objects.filter(last_staff_id=staff.staff_id).last()
        id_generator.status = 's'
        id_generator.save()

        category = 'staff_registration'
        subject = "{} just completed staff registration".format(staff.__str__().title())
        recent_activity = RecentActivityModel.objects.create(category=category, subject=subject,
                                                             reference_id=staff.id,
                                                             user=staff.created_by)
        recent_activity.save()
