from django.contrib import admin
from training.models import LessonMaterialModel, EnrollmentModel


admin.site.register(LessonMaterialModel)
admin.site.register(EnrollmentModel)