import base64

import pytz
from django.utils.timezone import make_aware
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.urls import reverse
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from human_resource.models import StaffModel
from training.models import LessonModel, CourseModel, LiveSessionModel
import requests
from django.conf import settings
from datetime import datetime, timedelta
import json
from training.views import get_zoom_access_token


class HomePageView(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lesson_list'] = LessonModel.objects.all()[:5]
        context['course_list'] = CourseModel.objects.all()[:3]
        return context


class AboutPageView(TemplateView):
    template_name = 'home/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TrainerPageView(TemplateView):
    template_name = 'home/trainer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trainer_list'] = StaffModel.objects.filter(is_trainer=True)
        return context


class ContactPageView(TemplateView):
    template_name = 'home/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def login_view(request):
    if request.method == 'POST':
        pass

    return render(request, 'home/login.html')


def pre_login_view(request):
    if request.method == 'POST':
        intended_url = request.POST.get('next')
    else:
        intended_url = request.GET.get('next')

    if 'myadmin' in intended_url.lower():
        return redirect('admin_login')
    return redirect('student_login')


def get_zoom_access_token():
    client_id = settings.ZOOM_CLIENT_ID
    client_secret = settings.ZOOM_CLIENT_SECRET
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

    token_url = "https://zoom.us/oauth/token"
    headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials'
    }

    response = requests.post(token_url, headers=headers, data=data)
    response_data = response.json()

    if response.status_code != 200:
        raise Exception(f"Failed to fetch access token: {response_data}")

    return response_data['access_token']

def test_session(request):
    try:
        access_token = get_zoom_access_token()
        return HttpResponse(access_token)
    except Exception as e:
        return render(request, 'error.html', {'message': str(e)})

    live_session = LiveSessionModel.objects.first()
    if not live_session:
        return render(request, 'error.html', {'message': 'No live session found'})

    topic = live_session.title
    duration = live_session.duration

    zoom_api_url = "https://api.zoom.us/v2/users/me/meetings"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    start_datetime = datetime.combine(live_session.session_date, live_session.session_time)
    start_datetime_aware = make_aware(start_datetime, timezone=pytz.UTC)

    meeting_details = {
        "topic": topic,
        "type": 2,  # Scheduled meeting
        "start_time": start_datetime_aware.isoformat(),  # ISO format required by Zoom
        "duration": duration,
        "timezone": "UTC"
    }

    response = requests.post(zoom_api_url, headers=headers, data=json.dumps(meeting_details))
    return HttpResponse(response)
    meeting_data = response.json()

    if response.status_code == 201:
        live_session.join_url = meeting_data.get('join_url', '')
        live_session.start_url = meeting_data.get('start_url', '')
        live_session.save()
        return render(request, 'success.html', {'message': 'Zoom meeting created successfully'})
    else:
        return render(request, 'error.html', {'message': f"Error creating Zoom meeting: {response.status_code}, {response.text}"})
