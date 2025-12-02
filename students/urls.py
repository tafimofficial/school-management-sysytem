from django.urls import path
from .views import (
    student_list, student_detail, student_create, 
    student_update, student_delete, get_students
)

urlpatterns = [
    path('', student_list, name='student_list'),
    path('create/', student_create, name='student_create'),
    path('<int:pk>/', student_detail, name='student_detail'),
    path('<int:pk>/edit/', student_update, name='student_update'),
    path('<int:pk>/delete/', student_delete, name='student_delete'),
    path('api/students/', get_students, name='get_students'),
]
