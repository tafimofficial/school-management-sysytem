from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Exam, ExamSchedule, Result
from .forms import ExamForm, ExamScheduleForm, ResultForm
from students.models import Student
from academics.models import Class, Subject
from core.models import User

class ExamListView(LoginRequiredMixin, ListView):
    model = Exam
    template_name = 'examination/exam_list.html'
    context_object_name = 'exams'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.role == User.Role.STUDENT:
            if hasattr(user, 'student_profile') and user.student_profile.current_class:
                # Filter exams that have schedules for the student's class
                return queryset.filter(schedules__exam_class=user.student_profile.current_class).distinct()
            return queryset.none()
        return queryset

class ExamCreateView(LoginRequiredMixin, CreateView):
    model = Exam
    form_class = ExamForm
    template_name = 'examination/exam_form.html'
    success_url = reverse_lazy('exam_list')

    def form_valid(self, form):
        messages.success(self.request, 'Exam created successfully.')
        return super().form_valid(form)

class ExamScheduleListView(LoginRequiredMixin, ListView):
    model = ExamSchedule
    template_name = 'examination/schedule_list.html'
    context_object_name = 'schedules'

class ExamScheduleCreateView(LoginRequiredMixin, CreateView):
    model = ExamSchedule
    form_class = ExamScheduleForm
    template_name = 'examination/schedule_form.html'
    success_url = reverse_lazy('schedule_list')

    def form_valid(self, form):
        messages.success(self.request, 'Schedule created successfully.')
        return super().form_valid(form)

class ResultEntryView(LoginRequiredMixin, View):
    template_name = 'examination/result_entry.html'

    def get(self, request):
        exams = Exam.objects.filter(is_active=True)
        classes = Class.objects.all()
        subjects = Subject.objects.all()
        return render(request, self.template_name, {
            'exams': exams, 'classes': classes, 'subjects': subjects
        })

    def post(self, request):
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
            
        return render(request, self.template_name)
