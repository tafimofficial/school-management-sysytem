from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Attendance, LeaveApplication
from .forms import AttendanceForm, LeaveApplicationForm
from students.models import Student
from academics.models import Class, Section

class AttendanceDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'attendance/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today_attendance'] = Attendance.objects.filter(date=timezone.now().date()).count()
        context['pending_leaves'] = LeaveApplication.objects.filter(status='PENDING').count()
        return context

class MarkAttendanceView(LoginRequiredMixin, View):
    template_name = 'attendance/mark_attendance.html'

    def get(self, request):
        classes = Class.objects.all()
        return render(request, self.template_name, {'classes': classes})

    def post(self, request):
        class_id = request.POST.get('class_id')
        section_id = request.POST.get('section_id')
        date = request.POST.get('date')
        
        if class_id and section_id and date:
            students = Student.objects.filter(current_class_id=class_id, section_id=section_id)
            
            for student in students:
                status = request.POST.get(f'status_{student.id}')
                remarks = request.POST.get(f'remarks_{student.id}')
                
                Attendance.objects.update_or_create(
                    student=student,
                    date=date,
                    defaults={
                        'status': status,
                        'remarks': remarks,
                        'recorded_by': request.user
                    }
                )
            messages.success(request, 'Attendance marked successfully.')
            return redirect('attendance_dashboard')
            
        return render(request, self.template_name, {'classes': Class.objects.all()})

class LeaveApplicationListView(LoginRequiredMixin, ListView):
    model = LeaveApplication
    template_name = 'attendance/leave_list.html'
    context_object_name = 'leaves'

    def get_queryset(self):
        if self.request.user.role in ['SUPER_ADMIN', 'SCHOOL_ADMIN']:
            return LeaveApplication.objects.all()
        return LeaveApplication.objects.filter(user=self.request.user)

class LeaveApplicationCreateView(LoginRequiredMixin, CreateView):
    model = LeaveApplication
    form_class = LeaveApplicationForm
    template_name = 'attendance/leave_form.html'
    success_url = reverse_lazy('leave_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Leave application submitted.')
        return super().form_valid(form)

class LeaveStatusUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if request.user.role not in ['SUPER_ADMIN', 'SCHOOL_ADMIN']:
            messages.error(request, 'You do not have permission to perform this action.')
            return redirect('leave_list')
            
        leave = get_object_or_404(LeaveApplication, pk=pk)
        action = request.POST.get('action')
        
        if action == 'approve':
            leave.status = 'APPROVED'
            messages.success(request, 'Leave application approved.')
        elif action == 'reject':
            leave.status = 'REJECTED'
            messages.success(request, 'Leave application rejected.')
            
        leave.save()
        return redirect('leave_list')
