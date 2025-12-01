from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Class, Section, Subject, TeacherSubjectAssignment, AcademicYear
from .forms import TeacherAssignmentForm

# Class Views
class ClassListView(LoginRequiredMixin, ListView):
    model = Class
    template_name = 'academics/class_list.html'
    context_object_name = 'classes'

class ClassCreateView(LoginRequiredMixin, CreateView):
    model = Class
    fields = ['name', 'numeric_value']
    template_name = 'academics/class_form.html'
    success_url = reverse_lazy('class_list')

    def form_valid(self, form):
        messages.success(self.request, 'Class created successfully.')
        return super().form_valid(form)

class ClassDeleteView(LoginRequiredMixin, DeleteView):
    model = Class
    template_name = 'academics/class_confirm_delete.html'
    success_url = reverse_lazy('class_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Class deleted successfully.')
        return super().delete(request, *args, **kwargs)

class ClassDetailView(LoginRequiredMixin, DetailView):
    model = Class
    template_name = 'academics/class_detail.html'
    context_object_name = 'class_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        class_obj = self.get_object()
        context['subjects'] = class_obj.subjects.all()
        # Get teachers who teach sections in this class
        context['teachers'] = TeacherSubjectAssignment.objects.filter(section__class_name=class_obj).select_related('teacher', 'subject', 'section')
        # Placeholder for routine
        context['routine'] = "Routine module not yet implemented."
        return context

# Section Views
class SectionCreateView(LoginRequiredMixin, CreateView):
    model = Section
    fields = ['name', 'class_name', 'class_teacher']
    template_name = 'academics/section_form.html'
    success_url = reverse_lazy('class_list') # Redirect to class list for now

    def form_valid(self, form):
        messages.success(self.request, 'Section created successfully.')
        return super().form_valid(form)

class SectionDeleteView(LoginRequiredMixin, DeleteView):
    model = Section
    template_name = 'academics/section_confirm_delete.html'
    success_url = reverse_lazy('class_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Section deleted successfully.')
        return super().delete(request, *args, **kwargs)

def get_sections(request):
    class_id = request.GET.get('class_id')
    sections = Section.objects.filter(class_name_id=class_id).values('id', 'name')
    
    # Filter out duplicates by name (case-insensitive and stripped) using dict comprehension
    # This keeps the last occurrence of each name. To keep the first, we'd need to reverse first.
    import re
    unique_sections_map = {}
    for section in sections:
        # Normalize: remove all non-alphanumeric characters and lowercase
        # This handles invisible characters, extra spaces, etc.
        name = re.sub(r'[^a-zA-Z0-9]', '', section['name']).lower()
        if name not in unique_sections_map:
            unique_sections_map[name] = section
            
    return JsonResponse(list(unique_sections_map.values()), safe=False)
            
    return JsonResponse(list(unique_sections_map.values()), safe=False)

# Subject Views
class SubjectListView(LoginRequiredMixin, ListView):
    model = Subject
    template_name = 'academics/subject_list.html'
    context_object_name = 'subjects'

class SubjectCreateView(LoginRequiredMixin, CreateView):
    model = Subject
    fields = ['name', 'code', 'classes', 'is_elective']
    template_name = 'academics/subject_form.html'
    template_name = 'academics/subject_form.html'
    success_url = reverse_lazy('subject_list')

    def get_initial(self):
        initial = super().get_initial()
        class_id = self.request.GET.get('class_id')
        if class_id:
            initial['classes'] = [class_id]
        return initial

    def get_success_url(self):
        class_id = self.request.GET.get('class_id')
        if class_id:
            return reverse_lazy('class_detail', kwargs={'pk': class_id})
        return reverse_lazy('subject_list')

    def form_valid(self, form):
        messages.success(self.request, 'Subject created successfully.')
        return super().form_valid(form)

class SubjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Subject
    template_name = 'academics/subject_confirm_delete.html'
    success_url = reverse_lazy('subject_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Subject deleted successfully.')
        return super().delete(request, *args, **kwargs)

# Academic Year Views
class AcademicYearListView(LoginRequiredMixin, ListView):
    model = AcademicYear
    template_name = 'academics/academic_year_list.html'
    context_object_name = 'academic_years'

class AcademicYearCreateView(LoginRequiredMixin, CreateView):
    model = AcademicYear
    fields = ['name', 'start_date', 'end_date', 'is_active']
    template_name = 'academics/academic_year_form.html'
    success_url = reverse_lazy('academic_year_list')

    def form_valid(self, form):
        messages.success(self.request, 'Academic Year created successfully.')
        return super().form_valid(form)

class TeacherAssignmentCreateView(LoginRequiredMixin, CreateView):
    model = TeacherSubjectAssignment
    form_class = TeacherAssignmentForm
    template_name = 'academics/teacher_assignment_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['class_id'] = self.request.GET.get('class_id')
        return kwargs

    def get_success_url(self):
        class_id = self.request.GET.get('class_id')
        if class_id:
            return reverse_lazy('class_detail', kwargs={'pk': class_id})
        return reverse_lazy('class_list')

    def form_valid(self, form):
        messages.success(self.request, 'Teacher assigned successfully.')
        return super().form_valid(form)
