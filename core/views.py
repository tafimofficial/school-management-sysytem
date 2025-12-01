from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import User
from academics.models import Class, Subject
from .forms import CustomUserCreationForm, CustomUserChangeForm

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role in [User.Role.SUPER_ADMIN, User.Role.SCHOOL_ADMIN]

class HomeView(TemplateView):
    template_name = 'home.html'

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['role'] = user.role
        
        if user.role in [User.Role.SUPER_ADMIN, User.Role.SCHOOL_ADMIN]:
            context['total_users'] = User.objects.count()
            context['total_students'] = User.objects.filter(role=User.Role.STUDENT).count()
            context['total_teachers'] = User.objects.filter(role=User.Role.TEACHER).count()
            context['total_classes'] = Class.objects.count()
            context['total_subjects'] = Subject.objects.count()
            context['recent_users'] = User.objects.order_by('-date_joined')[:5]
        
        elif user.role == User.Role.TEACHER:
            # Teacher specific context
            # Assuming teachers are linked to subjects/classes via TeacherSubjectAssignment or similar
            # For now, we'll show classes they teach if that relationship exists, or just general info
            pass
            
        elif user.role == User.Role.STUDENT:
            # Student specific context
            if hasattr(user, 'student_profile'):
                context['my_class'] = user.student_profile.current_class
                context['my_attendance'] = user.student_profile.attendance_records.count()
            pass
            
        return context

# User Management Views
class UserListView(AdminRequiredMixin, ListView):
    model = User
    template_name = 'core/user_list.html'
    context_object_name = 'users'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        role = self.request.GET.get('role')
        search_query = self.request.GET.get('q')
        
        if role:
            queryset = queryset.filter(role=role)
            
        if search_query:
            queryset = queryset.filter(
                username__icontains=search_query
            ) | queryset.filter(
                first_name__icontains=search_query
            ) | queryset.filter(
                last_name__icontains=search_query
            ) | queryset.filter(
                email__icontains=search_query
            )
            
        return queryset

class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'core/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.role == User.Role.STUDENT:
            # Import here to avoid circular import
            from students.models import Student
            from academics.models import Class
            student_profile, created = Student.objects.get_or_create(
                user=self.request.user,
                defaults={
                    'admission_number': self.request.user.username,
                    'admission_date': timezone.now().date(),
                    'date_of_birth': timezone.now().date(),
                    'gender': 'O',
                    'address': 'Not Provided',
                }
            )
            context['classes'] = Class.objects.all()
            context['student_profile'] = student_profile
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.role == User.Role.STUDENT:
            from students.models import Student
            from academics.models import Class
            class_id = self.request.POST.get('current_class')
            if class_id:
                student_profile, created = Student.objects.get_or_create(
                    user=self.request.user,
                    defaults={
                        'admission_number': self.request.user.username,
                        'admission_date': timezone.now().date(),
                        'date_of_birth': timezone.now().date(),
                        'gender': 'O',
                        'address': 'Not Provided',
                    }
                )
                student_profile.current_class = Class.objects.get(id=class_id)
                student_profile.save()
        messages.success(self.request, 'Profile updated successfully.')
        return response

class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'core/settings.html'

class UserCreateView(AdminRequiredMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'core/user_form.html'
    success_url = reverse_lazy('user_list')

    def form_valid(self, form):
        messages.success(self.request, 'User created successfully.')
        return super().form_valid(form)

class UserUpdateView(AdminRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'core/user_form.html'
    success_url = reverse_lazy('user_list')

    def form_valid(self, form):
        messages.success(self.request, 'User updated successfully.')
        return super().form_valid(form)

class UserDeleteView(AdminRequiredMixin, DeleteView):
    model = User
    template_name = 'core/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'User deleted successfully.')
        return super().delete(request, *args, **kwargs)
