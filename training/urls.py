from django.urls import path
from training.views import *

urlpatterns = [
    path('course/create', CourseCreateView.as_view(), name='course_create'),
    path('course/index', CourseListView.as_view(), name='course_index'),
    path('course/<int:pk>/detail', CourseDetailView.as_view(), name='course_detail'),
    path('course/<int:pk>/edit', CourseUpdateView.as_view(), name='course_edit'),
    path('course/<int:pk>/delete', CourseDeleteView.as_view(), name='course_delete'),

    path('lesson/create', LessonCreateView.as_view(), name='lesson_create'),
    path('lesson/index', LessonListView.as_view(), name='lesson_index'),
    path('lesson/<int:pk>/detail', LessonDetailView.as_view(), name='lesson_detail'),
    path('lesson/<int:pk>/edit', LessonUpdateView.as_view(), name='lesson_edit'),
    path('lesson/<int:pk>/delete', LessonDeleteView.as_view(), name='lesson_delete'),

    path('lesson/<int:pk>/material/create', LessonMaterialCreateView.as_view(), name='lesson_material_create'),
    path('lesson/<int:pk>/material/note/create', LessonMaterialNoteCreateView.as_view(), name='lesson_material_note_create'),
    path('lesson/material/index', LessonMaterialListView.as_view(), name='lesson_material_index'),
    path('lesson/material/<int:pk>/detail', LessonMaterialDetailView.as_view(), name='lesson_material_detail'),
    path('lesson/material/<int:pk>/edit', LessonMaterialUpdateView.as_view(), name='lesson_material_edit'),
    path('lesson/<int:pk>/material/note/edit', LessonMaterialNoteUpdateView.as_view(),
         name='lesson_material_note_edit'),

    path('lesson/material/<int:pk>/delete', LessonMaterialDeleteView.as_view(), name='lesson_material_delete'),

    path('live-session/create', LiveSessionCreateView.as_view(), name='live_session_create'),
    path('live-session/index', LiveSessionListView.as_view(), name='live_session_index'),
    path('live-session/<int:pk>/detail', LiveSessionDetailView.as_view(), name='live_session_detail'),
    path('live-session/<int:pk>/edit', LiveSessionUpdateView.as_view(), name='live_session_edit'),
    path('live-session/<int:pk>/delete', LiveSessionDeleteView.as_view(), name='live_session_delete'),
]

