# Generated by Django 5.0 on 2024-09-15 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0018_alter_progressmodel_progress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livesessionmodel',
            name='duration',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
