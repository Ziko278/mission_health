# Generated by Django 5.0 on 2024-07-09 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0016_progressmodel_delete_progresstracking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progressmodel',
            name='progress',
            field=models.JSONField(default='{}', verbose_name={}),
            preserve_default=False,
        ),
    ]