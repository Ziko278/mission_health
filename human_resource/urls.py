from django.urls import path
from human_resource.views import *

urlpatterns = [

    path('setting/create', HRSettingCreateView.as_view(), name='hr_setting_create'),
    path('setting/<int:pk>/detail', HRSettingDetailView.as_view(), name='hr_setting_detail'),
    path('setting/<int:pk>/edit', HRSettingUpdateView.as_view(), name='hr_setting_edit'),

    path('position/add', PositionCreateView.as_view(), name='position_create'),
    path('position/index', PositionListView.as_view(), name='position_index'),
    path('position/<int:pk>/detail', PositionDetailView.as_view(), name='position_detail'),
    path('position/<int:pk>/edit', PositionUpdateView.as_view(), name='position_edit'),
    path('position/<int:pk>/permission/edit', position_permission_view, name='position_permission'),
    path('position/<int:pk>/delete', PositionDeleteView.as_view(), name='position_delete'),

    path('staff/create', StaffCreateView.as_view(), name='staff_create'),
    path('staff/index', StaffListView.as_view(), name='staff_index'),
    path('staff/<int:pk>/detail', StaffDetailView.as_view(), name='staff_detail'),
    path('staff/<int:pk>/edit', StaffUpdateView.as_view(), name='staff_edit'),
    path('staff/<int:pk>/delete', StaffDeleteView.as_view(), name='staff_delete'),

]
