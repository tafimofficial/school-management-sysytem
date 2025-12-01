from django.urls import path
from .views import (
    ExamListView, ExamCreateView,
    ExamScheduleListView, ExamScheduleCreateView,
    ResultEntryView
)

urlpatterns = [
    path('exams/', ExamListView.as_view(), name='exam_list'),
    path('exams/add/', ExamCreateView.as_view(), name='exam_create'),
    path('schedule/', ExamScheduleListView.as_view(), name='schedule_list'),
    path('schedule/add/', ExamScheduleCreateView.as_view(), name='schedule_create'),
    path('results/entry/', ResultEntryView.as_view(), name='result_entry'),
]
