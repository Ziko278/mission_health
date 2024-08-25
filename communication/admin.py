from django.contrib import admin
from communication.models import RecentActivityModel, MessageModel, StudentMessageModel

admin.site.register(RecentActivityModel)
admin.site.register(MessageModel)
admin.site.register(StudentMessageModel)
