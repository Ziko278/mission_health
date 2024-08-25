# Generated by Django 5.0 on 2024-06-10 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0002_remove_coursemodel_status_coursemodel_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessonmaterialmodel',
            name='order',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lessonmaterialmodel',
            name='material_type',
            field=models.CharField(blank=True, choices=[('pdf', 'PDF'), ('video', 'VIDEO'), ('note', 'NOTE')], max_length=50, null=True),
        ),
    ]
