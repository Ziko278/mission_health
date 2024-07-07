from django.contrib import admin
from communication.models import RecentActivityModel, MessageModel

admin.site.register(RecentActivityModel)
admin.site.register(MessageModel)