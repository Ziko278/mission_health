# Generated by Django 5.0 on 2024-06-12 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_rename_staff_studentprofilemodel_student'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentprofilemodel',
            old_name='stUDENT',
            new_name='student',
        ),
    ]
