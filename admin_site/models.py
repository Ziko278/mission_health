from django.db import models
from django.contrib.auth.models import User


class DaysModel(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name.upper()


class SiteInfoModel(models.Model):
    name = models.CharField(max_length=150)
    short_name = models.CharField(max_length=50)
    mobile_1 = models.CharField(max_length=20)
    mobile_2 = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=255, null=True, blank=True)

    logo = models.FileField(upload_to='images/setting/logo')

    # social media handles
    whatsapp_number = models.CharField(max_length=100, null=True, blank=True)
    facebook_handle = models.URLField(max_length=100, null=True, blank=True)
    twitter_handle = models.URLField(max_length=100, null=True, blank=True)
    linkedin_handle = models.URLField(max_length=100, null=True, blank=True)
    youtube_handle = models.URLField(max_length=100, null=True, blank=True)

    primary_color = models.CharField(max_length=255)
    secondary_color = models.CharField(max_length=255)

    def __str__(self):
        return self.short_name.upper()


class CountryModel(models.Model):
    """  """
    name = models.CharField(max_length=100, unique=True)
    long_code_name = models.CharField(max_length=100, unique=True)
    short_code_name = models.CharField(max_length=100, unique=True)
    country_code = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    STATUS = (
        ('active', 'ACTIVE'), ('inactive', 'INACTIVE')
    )
    status = models.CharField(max_length=15, blank=True, choices=STATUS, default='active')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name.upper()


class ProfessionModel(models.Model):
    """"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name.upper()








