from django.urls import path
from .views import (
    exam_list, exam_create, exam_update, exam_delete,
    schedule_list, schedule_create,
    result_entry, my_results, class_results,
    result_edit, result_delete
)

urlpatterns = [
    path('exams/', exam_list, name='exam_list'),
    path('exams/add/', exam_create, name='exam_create'),
    path('exams/<int:pk>/edit/', exam_update, name='exam_update'),
    path('exams/<int:pk>/delete/', exam_delete, name='exam_delete'),
    path('schedule/', schedule_list, name='schedule_list'),
    path('schedule/add/', schedule_create, name='schedule_create'),
    path('results/entry/', result_entry, name='result_entry'),
    path('results/my/', my_results, name='my_results'),
    path('results/class/', class_results, name='class_results'),
    path('results/<int:pk>/edit/', result_edit, name='result_edit'),
    path('results/<int:pk>/delete/', result_delete, name='result_delete'),
]
