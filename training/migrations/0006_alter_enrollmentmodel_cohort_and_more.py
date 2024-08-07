# Generated by Django 5.0 on 2024-07-03 05:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0009_remove_studentsmodel_middle_name'),
        ('training', '0005_enrollmentmodel_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollmentmodel',
            name='cohort',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='student.cohortmodel'),
        ),
        migrations.AlterField(
            model_name='enrollmentmodel',
            name='status',
            field=models.CharField(blank=True, choices=[('active', 'ACTIVE'), ('inactive', 'INACTIVE')], default='active', max_length=10, null=True),
        ),
    ]
