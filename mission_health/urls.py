from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('', include('front_cms.urls')),
    path('myadmin/', include('admin_site.urls')),
    path('myadmin/communication/', include('communication.urls')),
    path('myadmin/finance/', include('finance.urls')),
    path('', include('home.urls')),
    path('myadmin/human-resource/', include('human_resource.urls')),
    path('myadmin/student/', include('student.urls')),
    path('student/', include('student_portal.urls')),
    path('myadmin/training/', include('training.urls')),
    path('django-admin/', admin.site.urls),

    # path('', HomePageView.as_view(), name='homepage'),
    # path('about-us', AboutPageView.as_view(), name='about'),
    # path('contact-us', ContactPageView.as_view(), name='contact_us'),
    # path('our-staff', StaffPageView.as_view(), name='our_staff'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
