from django.urls import path
from admin_site.views import *

urlpatterns = [
    path('', AdminDashboardView.as_view(), name='admin_dashboard'),

    path('site-info/create', SiteInfoCreateView.as_view(), name='site_info_create'),
    path('site-info/<int:pk>/detail', SiteInfoDetailView.as_view(), name='site_info_detail'),
    path('site-info/<int:pk>/edit', SiteInfoUpdateView.as_view(), name='site_info_edit'),

    path('country/create', CountryCreateView.as_view(), name='country_create'),
    path('country/index', CountryListView.as_view(), name='country_index'),
    path('country/<int:pk>/edit', CountryUpdateView.as_view(), name='country_edit'),
    path('country/<int:pk>/delete', CountryDeleteView.as_view(), name='country_delete'),

    path('profession/create', ProfessionCreateView.as_view(), name='profession_create'),
    path('profession/index', ProfessionListView.as_view(), name='profession_index'),
    path('profession/<int:pk>/edit', ProfessionUpdateView.as_view(), name='profession_edit'),
    path('profession/<int:pk>/delete', ProfessionDeleteView.as_view(), name='profession_delete'),


]

