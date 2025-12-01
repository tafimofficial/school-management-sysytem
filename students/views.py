from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Student
from .forms import StudentForm

class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                user__first_name__icontains=query
            ) | queryset.filter(
                user__last_name__icontains=query
            ) | queryset.filter(
                admission_number__icontains=query
            )
        return queryset

class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'students/student_detail.html'
    context_object_name = 'student'

class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        messages.success(self.request, 'Student created successfully.')
        return super().form_valid(form)

class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student_list')

    def get_initial(self):
        initial = super().get_initial()
        initial['first_name'] = self.object.user.first_name
        initial['last_name'] = self.object.user.last_name
        initial['email'] = self.object.user.email
        return initial

    def form_valid(self, form):
        messages.success(self.request, 'Student updated successfully.')
        return super().form_valid(form)

class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'students/student_confirm_delete.html'
    success_url = reverse_lazy('student_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Student deleted successfully.')
        return super().delete(request, *args, **kwargs)

def get_students(request):
    section_id = request.GET.get('section_id')
    class_id = request.GET.get('class_id')
    
    if section_id:
        students = Student.objects.filter(section_id=section_id).select_related('user')
    elif class_id:
        students = Student.objects.filter(current_class_id=class_id).select_related('user')
    else:
        students = Student.objects.none()
        
    # Filter out duplicates by name (case-insensitive and stripped) using dict comprehension
    unique_students_map = {}
    for s in students:
        full_name = s.user.get_full_name().strip()
        name_lower = full_name.lower()
        if name_lower not in unique_students_map:
            unique_students_map[name_lower] = {'id': s.id, 'name': full_name}
            
    return JsonResponse(list(unique_students_map.values()), safe=False)
