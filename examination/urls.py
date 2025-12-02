from django.urls import path
from .views import (
    exam_list, exam_create, exam_update, exam_delete,
    schedule_list, schedule_create,
    result_entry
)

urlpatterns = [
    path('exams/', exam_list, name='exam_list'),
    path('exams/add/', exam_create, name='exam_create'),
    path('exams/<int:pk>/edit/', exam_update, name='exam_update'),
    path('exams/<int:pk>/delete/', exam_delete, name='exam_delete'),
    path('schedule/', schedule_list, name='schedule_list'),
    path('schedule/add/', schedule_create, name='schedule_create'),
    path('results/entry/', result_entry, name='result_entry'),
]
