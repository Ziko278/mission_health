# Generated by Django 5.0 on 2024-06-13 17:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0010_remove_trainingpaymentmodel_account_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainingpaymentmodel',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='currency', to='finance.currencymodel'),
        ),
        migrations.AlterField(
            model_name='trainingpaymentmodel',
            name='default_currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='finance.currencymodel'),
        ),
    ]
