# Generated by Django 5.0 on 2024-07-07 12:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('human_resource', '0004_alter_staffmodel_email_alter_staffmodel_mobile'),
        ('training', '0010_alter_lessonmaterialmodel_lesson'),
    ]

    operations = [
        migrations.CreateModel(
            name='LiveSessionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('session_date', models.DateField()),
                ('session_time', models.TimeField()),
                ('duration', models.IntegerField()),
                ('meeting_id', models.CharField(max_length=50, unique=True)),
                ('join_url', models.URLField()),
                ('start_url', models.URLField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='live_sessions', to='training.coursemodel')),
                ('trainers', models.ManyToManyField(blank=True, to='human_resource.staffmodel')),
            ],
        ),
        migrations.DeleteModel(
            name='LiveSession',
        ),
    ]