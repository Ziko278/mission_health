from django.contrib.sites.shortcuts import get_current_site
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.http import urlsafe_base64_encode
from communication.views import account_activation_token, send_custom_email
from student.models import *
from django.contrib.auth.models import User
from training.models import LiveSessionModel
import requests
from django.conf import settings
from datetime import datetime, timedelta
import json
from training.views import get_zoom_access_token


@receiver(post_save, sender=LiveSessionModel)
def create_student_account(sender, instance, created, **kwargs):
    if created:
        live_session = instance
        access_token = get_zoom_access_token()

        topic = live_session.title
        start_time = live_session.start_date
        duration = live_session.duration

        access_token = 'ZOOM_CLIENT_ID'

        zoom_api_url = "https://api.zoom.us/v2/users/me/meetings"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        meeting_details = {
            "topic": topic,
            "type": 2,  # Scheduled meeting
            "start_time": start_time,
            "duration": duration,
            "timezone": "UTC"
        }

        response = requests.post(zoom_api_url, headers=headers, data=json.dumps(meeting_details))
        meeting_data = response.json()

        live_session.join_url = meeting_data['join_url'],
        live_session.start_url = meeting_data['start_url']
        live_session.save()

