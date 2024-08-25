from django.apps import apps
from django.db import models
from django.contrib.auth.models import User, Group
import random
from admin_site.models import CountryModel


class CohortModel(models.Model):
    name = models.CharField(max_length=250)
    cohort_id = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    STATUS = (
        ('0', 'Not Commenced'), ('1', 'In Progress'), ('2', 'Concluded')
    )
    status = models.CharField(max_length=50, choices=STATUS, default='0')

    def __str__(self):
        return self.name.upper()

    def student_count(self):
        return StudentsModel.objects.filter(cohort=self).count()


class StudentsModel(models.Model):
    """  """
    surname = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    registration_number = models.CharField(max_length=50, blank=True, null=True)
    GENDER = (
        ('male', 'MALE'), ('female', 'FEMALE')
    )
    gender = models.CharField(max_length=10, choices=GENDER)
    country = models.ForeignKey(CountryModel, null=True, on_delete=models.SET_NULL)
    state = models.CharField(max_length=100, null=True, blank=True)
    image = models.FileField(blank=True, null=True, upload_to='images/student_images')
    mobile = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    cohort = models.ForeignKey(CohortModel, null=True, on_delete=models.SET_NULL)

    registration_date = models.DateField(auto_now_add=True, blank=True, null=True)
    status = models.CharField(max_length=15, blank=True, default='active')
    study_status = models.CharField(max_length=15, blank=True, default='active')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f'{self.surname} {self.last_name}'

    def save(self, *args, **kwargs):

        if not self.registration_number:
            cohort = self.cohort
            last_student = StudentIDGeneratorModel.objects.filter(status='s').last()
            if last_student:
                student_id = str(int(last_student.last_id) + 1)
            else:
                student_id = str(1)
            while True:
                gen_id = student_id
                student_id = cohort.cohort_id + '-' + student_id.rjust(4, '0')
                student_exist = StudentsModel.objects.filter(registration_number=student_id).first()
                if not student_exist:
                    break
                else:
                    student_id = str(int(gen_id) + 1)
            self.registration_number = student_id

            generate_id = StudentIDGeneratorModel.objects.create(last_id=gen_id,
                                                                 last_student_id=self.registration_number,
                                                                 status='f')
            generate_id.save()

        if self.user:
            user = self.user
            user.email = self.email
            user.save()

        super(StudentsModel, self).save(*args, **kwargs)

    def my_course_list(self):
        enrollment_model = apps.get_model('training', 'EnrollmentModel')
        enrollment_list = enrollment_model.objects.filter(student=self, status='active')
        return [enrollment.course.id for enrollment in enrollment_list]


class StudentProfileModel(models.Model):
    """ This model relates staff to their username """
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, related_name='user_student_profile')
    student = models.OneToOneField(StudentsModel, on_delete=models.CASCADE, null=True, related_name='student_profile')
    default_password = models.CharField(max_length=100)

    def __str__(self):
        return self.student.__str__()


class StudentIDGeneratorModel(models.Model):
    last_id = models.IntegerField()
    last_student_id = models.CharField(max_length=100, null=True, blank=True)
    STATUS = (
        ('s', 'SUCCESS'), ('f', 'FAIL')
    )
    status = models.CharField(max_length=10, choices=STATUS, blank=True, default='f')


class StudentSettingModel(models.Model):
    auto_generate_student_id = models.BooleanField(default=True)

