# Generated by Django 5.0 on 2024-06-16 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0012_financesettingmodel_allow_part_payment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='financesettingmodel',
            name='current_access_payment',
            field=models.FloatField(default=50),
        ),
        migrations.AlterField(
            model_name='financesettingmodel',
            name='current_minimum_payment',
            field=models.FloatField(default=10),
        ),
    ]
