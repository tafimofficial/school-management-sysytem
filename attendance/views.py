from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .models import Attendance, LeaveApplication
from .forms import AttendanceForm, LeaveApplicationForm
from students.models import Student
from academics.models import Class, Section
from core.models import User
from django.core.paginator import Paginator

def is_admin(user):
    return user.is_authenticated and user.role in [User.Role.SUPER_ADMIN, User.Role.SCHOOL_ADMIN]

@login_required
def attendance_dashboard(request):
    context = {}
    context['today_attendance'] = Attendance.objects.filter(date=timezone.now().date()).count()
    context['pending_leaves'] = LeaveApplication.objects.filter(status='PENDING').count()
    return render(request, 'attendance/dashboard.html', context)

@login_required
def mark_attendance(request):
    if request.method == 'POST':
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
            
        return render(request, 'attendance/mark_attendance.html', {'classes': Class.objects.all()})
    else:
        classes = Class.objects.all()
        return render(request, 'attendance/mark_attendance.html', {'classes': classes})

@login_required
def leave_list(request):
    if request.user.role in [User.Role.SUPER_ADMIN, User.Role.SCHOOL_ADMIN]:
        leaves = LeaveApplication.objects.all()
    else:
        leaves = LeaveApplication.objects.filter(user=request.user)
    return render(request, 'attendance/leave_list.html', {'leaves': leaves})

@login_required
def leave_apply(request):
    if request.method == 'POST':
        form = LeaveApplicationForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.user = request.user
            leave.save()
            messages.success(request, 'Leave application submitted.')
            return redirect('leave_list')
    else:
        form = LeaveApplicationForm()
    return render(request, 'attendance/leave_form.html', {'form': form})

@login_required
def leave_update_status(request, pk):
    if request.user.role not in [User.Role.SUPER_ADMIN, User.Role.SCHOOL_ADMIN]:
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('leave_list')
        
    if request.method == 'POST':
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

@login_required
def attendance_report(request):
    queryset = Attendance.objects.all()
    
    # Filtering
    class_id = request.GET.get('class_id')
    section_id = request.GET.get('section_id')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    status = request.GET.get('status')

    if class_id:
        queryset = queryset.filter(student__current_class_id=class_id)
    if section_id:
        queryset = queryset.filter(student__section_id=section_id)
    if date_from:
        queryset = queryset.filter(date__gte=date_from)
    if date_to:
        queryset = queryset.filter(date__lte=date_to)
    if status:
        queryset = queryset.filter(status=status)
        
    queryset = queryset.select_related('student', 'student__current_class', 'student__section')
    
    paginator = Paginator(queryset, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'attendance_records': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'classes': Class.objects.all(),
        'sections': Section.objects.all()
    }
    return render(request, 'attendance/attendance_report.html', context)
