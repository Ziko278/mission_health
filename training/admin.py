from django.contrib import admin
from training.models import LessonMaterialModel, EnrollmentModel, LiveSessionModel, ProgressModel


admin.site.register(LessonMaterialModel)
admin.site.register(EnrollmentModel)
admin.site.register(LiveSessionModel)
admin.site.register(ProgressModel)