from django.urls import path
from .views import (
    attendance_dashboard, mark_attendance,
    leave_list, leave_apply,
    leave_update_status, attendance_report
)

urlpatterns = [
    path('', attendance_dashboard, name='attendance_dashboard'),
    path('mark/', mark_attendance, name='mark_attendance'),
    path('leaves/', leave_list, name='leave_list'),
    path('leaves/apply/', leave_apply, name='leave_apply'),
    path('leaves/<int:pk>/update/', leave_update_status, name='leave_update_status'),
    path('reports/', attendance_report, name='attendance_report'),
]
