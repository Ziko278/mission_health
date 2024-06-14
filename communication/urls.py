from django.urls import path
from communication.views import *

urlpatterns = [

    path('smtp-configuration/create', SMTPConfigurationCreateView.as_view(), name='smtp_configuration_create'),
    path('smtp-configuration/index', SMTPConfigurationListView.as_view(), name='smtp_configuration_index'),
    path('smtp-configuration/<int:pk>/edit', SMTPConfigurationUpdateView.as_view(), name='smtp_configuration_edit'),
    path('smtp-configuration/<int:pk>/delete', SMTPConfigurationDeleteView.as_view(), name='smtp_configuration_delete'),

    path('message/create', MessageCreateView.as_view(), name='message_create'),
    path('message/index', MessageListView.as_view(), name='message_index'),
    path('message/<int:pk>/edit', MessageUpdateView.as_view(), name='message_edit'),
    path('message/<int:pk>/delete', MessageDeleteView.as_view(), name='message_delete'),
    
    path('communication-setting/create', CommunicationSettingCreateView.as_view(), name='communication_setting_create'),
    path('communication-setting/<int:pk>/detail', CommunicationSettingDetailView.as_view(), name='communication_setting_detail'),
    path('communication-setting/<int:pk>/edit', CommunicationSettingUpdateView.as_view(), name='communication_setting_edit'),



]

