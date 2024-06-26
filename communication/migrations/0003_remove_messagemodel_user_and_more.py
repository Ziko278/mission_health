# Generated by Django 5.0 on 2024-06-12 08:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communication', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messagemodel',
            name='user',
        ),
        migrations.RemoveField(
            model_name='smsconfigurationmodel',
            name='user',
        ),
        migrations.RemoveField(
            model_name='smtpconfigurationmodel',
            name='staff',
        ),
        migrations.RemoveField(
            model_name='smtpconfigurationmodel',
            name='user',
        ),
        migrations.AlterField(
            model_name='recentactivitymodel',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='CommunicationSettingModel',
        ),
        migrations.DeleteModel(
            name='MessageModel',
        ),
        migrations.DeleteModel(
            name='SMSConfigurationModel',
        ),
        migrations.DeleteModel(
            name='SMTPConfigurationModel',
        ),
    ]
