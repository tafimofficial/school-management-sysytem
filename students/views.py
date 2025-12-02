from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student
from .forms import StudentForm
from django.core.paginator import Paginator
from django.db.models import Q

@login_required
def student_list(request):
    queryset = Student.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(admission_number__icontains=query)
        )
    
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'students/student_list.html', {'students': page_obj, 'page_obj': page_obj, 'is_paginated': page_obj.has_other_pages()})

@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/student_detail.html', {'student': student})

@login_required
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student created successfully.')
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'students/student_form.html', {'form': form})

@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    initial = {
        'first_name': student.user.first_name,
        'last_name': student.user.last_name,
        'email': student.user.email
    }
    
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully.')
            return redirect('student_list')
    else:
        form = StudentForm(instance=student, initial=initial)
    return render(request, 'students/student_form.html', {'form': form})

@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully.')
        return redirect('student_list')
    return render(request, 'students/student_confirm_delete.html', {'object': student})

def get_students(request):
    section_id = request.GET.get('section_id')
    class_id = request.GET.get('class_id')
    
    if section_id:
        students = Student.objects.filter(section_id=section_id).select_related('user')
    elif class_id:
        students = Student.objects.filter(current_class_id=class_id).select_related('user')
    else:
        students = Student.objects.none()
        
    unique_students_map = {}
    for s in students:
        full_name = s.user.get_full_name().strip()
        name_lower = full_name.lower()
        if name_lower not in unique_students_map:
            unique_students_map[name_lower] = {'id': s.id, 'name': full_name}
            
    return JsonResponse(list(unique_students_map.values()), safe=False)
