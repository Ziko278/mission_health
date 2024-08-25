# Generated by Django 5.0 on 2024-07-06 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communication', '0004_messagemodel_smtpconfigurationmodel_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='smtpconfigurationmodel',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='smtpconfigurationmodel',
            name='username',
        ),
        migrations.AddField(
            model_name='smtpconfigurationmodel',
            name='use_tls',
            field=models.BooleanField(default=True),
        ),
    ]