from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Exam, ExamSchedule, Result
from .forms import ExamForm, ExamScheduleForm, ResultForm, ExamScheduleFormSet
from students.models import Student
from academics.models import Class, Subject, Section
from core.models import User
from django.db.models import Q

@login_required
def exam_list(request):
    queryset = Exam.objects.all()
    user = request.user
    
    if user.role == User.Role.STUDENT:
        if hasattr(user, 'student_profile') and user.student_profile.current_class:
            queryset = queryset.filter(exam_class=user.student_profile.current_class)
            queryset = queryset.filter(
                Q(section__isnull=True) | Q(section=user.student_profile.section)
            )
            queryset = queryset.distinct()
        else:
            queryset = queryset.none()
    else:
        # For Admins/Teachers, allow filtering
        class_id = request.GET.get('class_id')
        section_id = request.GET.get('section_id')
        
        if class_id:
            queryset = queryset.filter(exam_class_id=class_id)
        if section_id:
            queryset = queryset.filter(section_id=section_id)
            
    context = {'exams': queryset}
    if user.role in [User.Role.SUPER_ADMIN, User.Role.SCHOOL_ADMIN, User.Role.TEACHER]:
        context['classes'] = Class.objects.all()
        context['sections'] = Section.objects.all()
        
    return render(request, 'examination/exam_list.html', context)

@login_required
def exam_create(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        schedules = ExamScheduleFormSet(request.POST)
        
        if form.is_valid() and schedules.is_valid():
            exam = form.save()
            schedules.instance = exam
            schedules.save()
            messages.success(request, 'Exam created successfully.')
            return redirect('exam_list')
    else:
        form = ExamForm()
        schedules = ExamScheduleFormSet()
        
    return render(request, 'examination/exam_form.html', {'form': form, 'schedules': schedules})

@login_required
def exam_update(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        schedules = ExamScheduleFormSet(request.POST, instance=exam)
        
        if form.is_valid() and schedules.is_valid():
            form.save()
            schedules.save()
            messages.success(request, 'Exam updated successfully.')
            return redirect('exam_list')
    else:
        form = ExamForm(instance=exam)
        schedules = ExamScheduleFormSet(instance=exam)
        
    return render(request, 'examination/exam_form.html', {'form': form, 'schedules': schedules})

@login_required
def exam_delete(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        exam.delete()
        messages.success(request, 'Exam deleted successfully.')
        return redirect('exam_list')
    return render(request, 'examination/exam_confirm_delete.html', {'object': exam})

@login_required
def schedule_list(request):
    schedules = ExamSchedule.objects.all()
    return render(request, 'examination/schedule_list.html', {'schedules': schedules})

@login_required
def schedule_create(request):
    if request.method == 'POST':
        form = ExamScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Schedule created successfully.')
            return redirect('schedule_list')
    else:
        form = ExamScheduleForm()
    return render(request, 'examination/schedule_form.html', {'form': form})

@login_required
def result_entry(request):
    if request.method == 'POST':
        exam_id = request.POST.get('exam_id')
        class_id = request.POST.get('class_id')
        subject_id = request.POST.get('subject_id')
        
        if exam_id and class_id and subject_id:
            students = Student.objects.filter(current_class_id=class_id)
            exam = Exam.objects.get(id=exam_id)
            subject = Subject.objects.get(id=subject_id)
            
            for student in students:
                marks = request.POST.get(f'marks_{student.id}')
                remarks = request.POST.get(f'remarks_{student.id}')
                
                if marks:
                    Result.objects.update_or_create(
                        exam=exam,
                        student=student,
                        subject=subject,
                        defaults={
                            'marks_obtained': marks,
                            'remarks': remarks
                        }
                    )
            messages.success(request, 'Results updated successfully.')
            return redirect('result_entry')
            
    exams = Exam.objects.filter(is_active=True)
    classes = Class.objects.all()
    subjects = Subject.objects.all()
    return render(request, 'examination/result_entry.html', {
        'exams': exams, 'classes': classes, 'subjects': subjects
    })
