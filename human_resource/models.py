from datetime import timedelta, date
from django.db import models, transaction
from django.contrib.auth.models import User, Group
from admin_site.model_info import *
from django.apps import apps
from admin_site.models import DaysModel


class StaffModel(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    image = models.ImageField(upload_to='images/staff', blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    mobile = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER)

    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    staff_id = models.CharField(max_length=100, blank=True, null=True)
    is_trainer = models.BooleanField(default=False, blank=True)

    status = models.CharField(max_length=30, blank=True, choices=STAFF_STATUS, default=STAFF_STATUS[0][0])

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='staff_created_by')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['staff_id'],
                name='unique_staff_id',
                violation_error_message='Staff with same Staff ID Already Exists',
            )
        ]

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            staff_setting = HRSettingModel.objects.first()

            if staff_setting.auto_generate_staff_id and not self.staff_id:
                self.generate_staff_id(staff_setting)

            if self.id:
                self.update_user_profile()

            if self.status.lower() != 'active':
                try:
                    user = StaffProfileModel.objects.get(staff=self).user
                    user.is_active = False
                    user.save()
                except Exception:
                    pass
            else:
                try:
                    user = StaffProfileModel.objects.get(staff=self).user
                    if not user.is_active:
                        user.is_active = False
                        user.save()
                except Exception:
                    pass

        super(StaffModel, self).save(*args, **kwargs)

    def generate_staff_id(self, staff_setting):

        last_staff = StaffIDGeneratorModel.objects.filter(status='s').last()
        if last_staff:
            staff_id = str(int(last_staff.last_id) + 1)
        else:
            staff_id = str(1)
        while True:
            gen_id = staff_id
            staff_id = staff_setting.staff_id_prefix + '-' + staff_id.rjust(4, '0')
            staff_exist = StaffModel.objects.filter(staff_id=staff_id).first()
            if not staff_exist:
                break
            else:
                staff_id = str(int(gen_id) + 1)
        self.staff_id = staff_id

        generate_id = StaffIDGeneratorModel.objects.create(last_id=gen_id, last_staff_id=self.staff_id, status='f')
        generate_id.save()

    def update_user_profile(self):
        user_profile = StaffProfileModel.objects.filter(staff=self).first()
        if user_profile:
            user = user_profile.user
            if self.email:
                user.email = self.email
            user.save()

            if self.group:
                self.group.user_set.add(user)

    def get_user_account(self):
        user = StaffProfileModel.objects.filter(staff=self).first().user
        return user


class StaffProfileModel(models.Model):
    """ This model relates staff to their username """
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, related_name='user_staff_profile')
    staff = models.OneToOneField(StaffModel, on_delete=models.CASCADE, null=True, related_name='staff_profile')
    default_password = models.CharField(max_length=100)

    def __str__(self):
        return self.staff.__str__()


class StaffIDGeneratorModel(models.Model):
    last_id = models.IntegerField()
    last_staff_id = models.CharField(max_length=100, null=True, blank=True)
    STATUS = (
        ('s', 'SUCCESS'), ('f', 'FAIL')
    )
    status = models.CharField(max_length=10, choices=STATUS, blank=True, default='f')


class HRSettingModel(models.Model):
    """This model handles all setting related to staff"""
    auto_generate_staff_id = models.BooleanField(default=True)
    auto_generate_logins = models.BooleanField(default=True)
    staff_id_prefix = models.CharField(max_length=10, blank=True, null=True)


class StaffReviewModel(models.Model):
    staff = models.ForeignKey(StaffModel, on_delete=models.CASCADE)
    # student = models.ForeignKey(StaffModel, on_delete=models.CASCADE)
    review = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


