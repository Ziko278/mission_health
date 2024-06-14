from django.urls import path
from home.views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),
    path('about', AboutPageView.as_view(), name='about_page'),
    path('contact', ContactPageView.as_view(), name='contact_page'),
    path('trainers', TrainerPageView.as_view(), name='trainer_page'),
    path('login', login_view, name='login'),

]

