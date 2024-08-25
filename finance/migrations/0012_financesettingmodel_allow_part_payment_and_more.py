# Generated by Django 5.0 on 2024-06-13 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0011_alter_trainingpaymentmodel_currency_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='financesettingmodel',
            name='allow_part_payment',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AddField(
            model_name='financesettingmodel',
            name='current_minimum_payment',
            field=models.FloatField(default=100),
        ),
    ]
