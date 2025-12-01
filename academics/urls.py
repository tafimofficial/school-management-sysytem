from django.urls import path
from .views import (
    ClassListView, ClassCreateView, SectionCreateView,
    ClassListView, ClassCreateView, SectionCreateView,
    SubjectListView, SubjectCreateView, ClassDetailView,
    get_sections, AcademicYearListView, AcademicYearCreateView,
    SectionDeleteView, ClassDeleteView, SubjectDeleteView,
    TeacherAssignmentCreateView
)

urlpatterns = [
    path('classes/', ClassListView.as_view(), name='class_list'),
    path('classes/<int:pk>/', ClassDetailView.as_view(), name='class_detail'),
    path('classes/create/', ClassCreateView.as_view(), name='class_create'),
    path('classes/<int:pk>/delete/', ClassDeleteView.as_view(), name='class_delete'),
    path('sections/create/', SectionCreateView.as_view(), name='section_create'),
    path('sections/<int:pk>/delete/', SectionDeleteView.as_view(), name='section_delete'),
    path('api/sections/', get_sections, name='get_sections'),
    path('subjects/', SubjectListView.as_view(), name='subject_list'),
    path('subjects/create/', SubjectCreateView.as_view(), name='subject_create'),
    path('subjects/<int:pk>/delete/', SubjectDeleteView.as_view(), name='subject_delete'),
    path('academic-years/', AcademicYearListView.as_view(), name='academic_year_list'),
    path('academic-years/', AcademicYearListView.as_view(), name='academic_year_list'),
    path('academic-years/create/', AcademicYearCreateView.as_view(), name='academic_year_create'),
    path('teacher-assignment/create/', TeacherAssignmentCreateView.as_view(), name='teacher_assign'),
]
