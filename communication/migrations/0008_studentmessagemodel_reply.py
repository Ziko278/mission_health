# Generated by Django 5.0 on 2024-07-12 01:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communication', '0007_studentmessagemodel_is_replied'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentmessagemodel',
            name='reply',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='replies', to='communication.studentmessagemodel'),
        ),
    ]
