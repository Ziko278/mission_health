# Generated by Django 5.0 on 2024-06-10 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0004_bankaccountmodel_use_global_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='financesettingmodel',
            name='auto_confirm_online_payment',
            field=models.BooleanField(blank=True, default=True),
        ),
    ]