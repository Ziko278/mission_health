from django.urls import path
from student.views import *

urlpatterns = [
    path('cohort/create', CohortCreateView.as_view(), name='cohort_create'),
    path('cohort/index', CohortListView.as_view(), name='cohort_index'),
    path('cohort/<int:pk>/detail', CohortDetailView.as_view(), name='cohort_detail'),
    path('cohort/<int:pk>/edit', CohortUpdateView.as_view(), name='cohort_edit'),
    path('cohort/<int:pk>/delete', CohortDeleteView.as_view(), name='cohort_delete'),

    path('register', StudentCreateView.as_view(), name='student_create'),
    path('index', StudentListView.as_view(), name='student_index'),
    path('alumni/index', StudentAlumniListView.as_view(), name='student_alumni_index'),
    path('<int:pk>/detail', StudentDetailView.as_view(), name='student_detail'),
    path('<int:pk>/edit', StudentUpdateView.as_view(), name='student_edit'),
    path('<int:pk>/delete', StudentDeleteView.as_view(), name='student_delete'),

]

