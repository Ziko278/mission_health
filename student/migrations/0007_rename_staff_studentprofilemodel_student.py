# Generated by Django 5.0 on 2024-06-12 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0006_studentprofilemodel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentprofilemodel',
            old_name='staff',
            new_name='stUDENT',
        ),
    ]
