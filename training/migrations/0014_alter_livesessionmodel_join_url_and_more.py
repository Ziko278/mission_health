# Generated by Django 5.0 on 2024-07-07 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0013_remove_livesessionmodel_trainers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livesessionmodel',
            name='join_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='livesessionmodel',
            name='meeting_id',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='livesessionmodel',
            name='start_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
