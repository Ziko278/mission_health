# Generated by Django 5.0 on 2024-06-06 19:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_site', '0002_siteinfomodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='siteinfomodel',
            name='author',
        ),
        migrations.RemoveField(
            model_name='siteinfomodel',
            name='description',
        ),
        migrations.RemoveField(
            model_name='siteinfomodel',
            name='emergency_contact',
        ),
        migrations.RemoveField(
            model_name='siteinfomodel',
            name='favicon',
        ),
        migrations.RemoveField(
            model_name='siteinfomodel',
            name='keywords',
        ),
        migrations.RemoveField(
            model_name='siteinfomodel',
            name='preloader',
        ),
        migrations.RemoveField(
            model_name='siteinfomodel',
            name='title',
        ),
    ]
