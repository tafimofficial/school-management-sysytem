from django.urls import path
from .views import (
    AttendanceDashboardView, MarkAttendanceView,
    LeaveApplicationListView, LeaveApplicationCreateView,
    LeaveStatusUpdateView
)

urlpatterns = [
    path('', AttendanceDashboardView.as_view(), name='attendance_dashboard'),
    path('mark/', MarkAttendanceView.as_view(), name='mark_attendance'),
    path('leaves/', LeaveApplicationListView.as_view(), name='leave_list'),
    path('leaves/apply/', LeaveApplicationCreateView.as_view(), name='leave_apply'),
    path('leaves/<int:pk>/update/', LeaveStatusUpdateView.as_view(), name='leave_update_status'),
]
