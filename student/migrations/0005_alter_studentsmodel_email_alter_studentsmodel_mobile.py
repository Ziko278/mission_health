# Generated by Django 5.0 on 2024-06-08 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_alter_cohortmodel_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentsmodel',
            name='email',
            field=models.EmailField(max_length=100),
        ),
        migrations.AlterField(
            model_name='studentsmodel',
            name='mobile',
            field=models.CharField(default='99', max_length=20),
            preserve_default=False,
        ),
    ]
