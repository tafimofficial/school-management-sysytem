from django.urls import path
from .views import (
    class_list, class_create, class_detail, class_delete,
    section_create, section_delete, get_sections, get_subjects,
    subject_list, subject_create, subject_delete,
    academic_year_list, academic_year_create,
    teacher_assign
)

urlpatterns = [
    path('classes/', class_list, name='class_list'),
    path('classes/<int:pk>/', class_detail, name='class_detail'),
    path('classes/create/', class_create, name='class_create'),
    path('classes/<int:pk>/delete/', class_delete, name='class_delete'),
    path('sections/create/', section_create, name='section_create'),
    path('sections/<int:pk>/delete/', section_delete, name='section_delete'),
    path('api/sections/', get_sections, name='get_sections'),
    path('api/subjects/', get_subjects, name='get_subjects'),
    path('subjects/', subject_list, name='subject_list'),
    path('subjects/create/', subject_create, name='subject_create'),
    path('subjects/<int:pk>/delete/', subject_delete, name='subject_delete'),
    path('academic-years/', academic_year_list, name='academic_year_list'),
    path('academic-years/create/', academic_year_create, name='academic_year_create'),
    path('teacher-assignment/create/', teacher_assign, name='teacher_assign'),
]
