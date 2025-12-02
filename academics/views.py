from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.contrib import messages
from .models import Class, Section, Subject, TeacherSubjectAssignment, AcademicYear
from .forms import TeacherAssignmentForm
from core.models import User
import re

def is_admin(user):
    return user.is_authenticated and user.role in [User.Role.SUPER_ADMIN, User.Role.SCHOOL_ADMIN]

# Class Views
@login_required
def class_list(request):
    classes = Class.objects.all()
    return render(request, 'academics/class_list.html', {'classes': classes})

@login_required
def class_create(request):
    from django.forms import modelform_factory
    ClassForm = modelform_factory(Class, fields=['name', 'numeric_value'])
    
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Class created successfully.')
            return redirect('class_list')
    else:
        form = ClassForm()
    return render(request, 'academics/class_form.html', {'form': form})

@login_required
def class_delete(request, pk):
    class_obj = get_object_or_404(Class, pk=pk)
    if request.method == 'POST':
        class_obj.delete()
        messages.success(request, 'Class deleted successfully.')
        return redirect('class_list')
    return render(request, 'academics/class_confirm_delete.html', {'object': class_obj})

@login_required
def class_detail(request, pk):
    class_obj = get_object_or_404(Class, pk=pk)
    subjects = class_obj.subjects.all()
    teachers = TeacherSubjectAssignment.objects.filter(section__class_name=class_obj).select_related('teacher', 'subject', 'section')
    routine = "Routine module not yet implemented."
    
    context = {
        'class_obj': class_obj,
        'subjects': subjects,
        'teachers': teachers,
        'routine': routine
    }
    return render(request, 'academics/class_detail.html', context)

# Section Views
@login_required
def section_create(request):
    from django.forms import modelform_factory
    SectionForm = modelform_factory(Section, fields=['name', 'class_name', 'class_teacher'])
    
    if request.method == 'POST':
        form = SectionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Section created successfully.')
            return redirect('class_list')
    else:
        form = SectionForm()
    return render(request, 'academics/section_form.html', {'form': form})

@login_required
def section_delete(request, pk):
    section = get_object_or_404(Section, pk=pk)
    if request.method == 'POST':
        section.delete()
        messages.success(request, 'Section deleted successfully.')
        return redirect('class_list')
    return render(request, 'academics/section_confirm_delete.html', {'object': section})

def get_sections(request):
    class_id = request.GET.get('class_id')
    sections = Section.objects.filter(class_name_id=class_id).values('id', 'name')
    
    unique_sections_map = {}
    for section in sections:
        name = re.sub(r'[^a-zA-Z0-9]', '', section['name']).lower()
        if name not in unique_sections_map:
            unique_sections_map[name] = section
            
    return JsonResponse(list(unique_sections_map.values()), safe=False)

def get_subjects(request):
    class_id = request.GET.get('class_id')
    subjects = Subject.objects.filter(classes__id=class_id).values('id', 'name')
    return JsonResponse(list(subjects), safe=False)

# Subject Views
@login_required
def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'academics/subject_list.html', {'subjects': subjects})

@login_required
def subject_create(request):
    from django.forms import modelform_factory
    SubjectForm = modelform_factory(Subject, fields=['name', 'code', 'classes', 'is_elective'])
    
    initial = {}
    class_id = request.GET.get('class_id')
    if class_id:
        initial['classes'] = [class_id]
        
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject created successfully.')
            if class_id:
                return redirect('class_detail', pk=class_id)
            return redirect('subject_list')
    else:
        form = SubjectForm(initial=initial)
    return render(request, 'academics/subject_form.html', {'form': form})

@login_required
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        subject.delete()
        messages.success(request, 'Subject deleted successfully.')
        return redirect('subject_list')
    return render(request, 'academics/subject_confirm_delete.html', {'object': subject})

# Academic Year Views
@login_required
def academic_year_list(request):
    academic_years = AcademicYear.objects.all()
    return render(request, 'academics/academic_year_list.html', {'academic_years': academic_years})

@login_required
@user_passes_test(is_admin)
def academic_year_create(request):
    from django.forms import modelform_factory
    AcademicYearForm = modelform_factory(AcademicYear, fields=['name', 'start_date', 'end_date', 'is_active'])
    
    if request.method == 'POST':
        form = AcademicYearForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Academic Year created successfully.')
            return redirect('academic_year_list')
    else:
        form = AcademicYearForm()
    return render(request, 'academics/academic_year_form.html', {'form': form})

@login_required
def teacher_assign(request):
    class_id = request.GET.get('class_id')
    
    if request.method == 'POST':
        form = TeacherAssignmentForm(request.POST, class_id=class_id)
        if form.is_valid():
            form.save()
            messages.success(request, 'Teacher assigned successfully.')
            if class_id:
                return redirect('class_detail', pk=class_id)
            return redirect('class_list')
    else:
        form = TeacherAssignmentForm(class_id=class_id)
    return render(request, 'academics/teacher_assignment_form.html', {'form': form})
