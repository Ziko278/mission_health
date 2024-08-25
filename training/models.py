from django.db import models
from django.contrib.auth.models import User, Group
import random
from admin_site.models import CountryModel
from human_resource.models import StaffModel
from student.models import StudentsModel, CohortModel


class CourseModel(models.Model):
    name = models.CharField(max_length=250)
    duration = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name.upper()


class LessonModel(models.Model):
    course = models.ForeignKey(CourseModel, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    description = models.TextField()
    order = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['course', 'order']


class EnrollmentModel(models.Model):
    student = models.ForeignKey(StudentsModel, on_delete=models.CASCADE)
    cohort = models.ForeignKey(CohortModel, on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey(CourseModel, on_delete=models.CASCADE)
    amount = models.FloatField(default=0, blank=True)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    STATUS = (
        ('active', 'ACTIVE'), ('inactive', 'INACTIVE')
    )
    status = models.CharField(max_length=10, choices=STATUS, blank=True, null=True, default='active')

    def save(self, *args, **kwargs):

        if not self.cohort:
            self.cohort = self.student.cohort

        if not self.amount or self.amount == 0:
            self.amount = self.course.amount

        super().save(*args, **kwargs)

    def __str__(self):
        return self.course.__str__()


class LessonMaterialModel(models.Model):
    lesson = models.ForeignKey(LessonModel, on_delete=models.CASCADE, related_name='materials')
    MATERIAL_TYPE = (('pdf', 'PDF'), ('video', 'VIDEO'), ('note', 'NOTE'))
    material_type = models.CharField(max_length=50, blank=True, null=True, choices=MATERIAL_TYPE)
    title = models.CharField(max_length=255)
    order = models.IntegerField(blank=True, null=True)
    introduction = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='training/material', null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Set material type based on file extension if a file is provided
        if self.file:
            extension = self.file.name.split('.')[-1].lower()
            if extension == 'pdf':
                self.material_type = 'pdf'
            elif extension in ['mp4', 'avi', 'mov']:
                self.material_type = 'video'

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class LiveSessionModel(models.Model):
    course = models.ForeignKey(CourseModel, on_delete=models.CASCADE, null=True, blank=True, related_name='live_sessions')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    session_date = models.DateField()
    session_time = models.TimeField()
    duration = models.IntegerField()
    meeting_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    join_url = models.URLField(blank=True, null=True)
    start_url = models.URLField(blank=True, null=True)


class ProgressModel(models.Model):
    student = models.ForeignKey(StudentsModel, on_delete=models.CASCADE, related_name='progress')
    cohort = models.ForeignKey(CohortModel, on_delete=models.CASCADE, blank=True, null=True)
    progress = models.JSONField(default={})


class Assignment(models.Model):
    lesson = models.ForeignKey(LessonModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()

    def __str__(self):
        return self.title
