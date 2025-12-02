from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import User
from academics.models import Class, Subject
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator

def is_admin(user):
    return user.is_authenticated and user.role in [User.Role.SUPER_ADMIN, User.Role.SCHOOL_ADMIN]

def home(request):
    return render(request, 'home.html')

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    user = request.user
    context = {'role': user.role}
    
    if user.role in [User.Role.SUPER_ADMIN, User.Role.SCHOOL_ADMIN]:
        context['total_users'] = User.objects.count()
        context['total_students'] = User.objects.filter(role=User.Role.STUDENT).count()
        context['total_teachers'] = User.objects.filter(role=User.Role.TEACHER).count()
        context['total_classes'] = Class.objects.count()
        context['total_subjects'] = Subject.objects.count()
        context['recent_users'] = User.objects.order_by('-date_joined')[:5]
    
    elif user.role == User.Role.TEACHER:
        pass
        
    elif user.role == User.Role.STUDENT:
        if hasattr(user, 'student_profile'):
            context['my_class'] = user.student_profile.current_class
            context['my_attendance'] = user.student_profile.attendance_records.count()
            
    return render(request, 'dashboard/dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def user_list(request):
    queryset = User.objects.all()
    role = request.GET.get('role')
    search_query = request.GET.get('q')
    
    if role:
        queryset = queryset.filter(role=role)
        
    if search_query:
        queryset = queryset.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
        
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'core/user_list.html', {'users': page_obj, 'page_obj': page_obj, 'is_paginated': page_obj.has_other_pages()})

@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            if user.role == User.Role.STUDENT:
                from students.models import Student
                from academics.models import Class
                class_id = request.POST.get('current_class')
                if class_id:
                    student_profile, created = Student.objects.get_or_create(
                        user=user,
                        defaults={
                            'admission_number': user.username,
                            'admission_date': timezone.now().date(),
                            'date_of_birth': timezone.now().date(),
                            'gender': 'O',
                            'address': 'Not Provided',
                        }
                    )
                    student_profile.current_class = Class.objects.get(id=class_id)
                    student_profile.save()
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=user)
    
    context = {'form': form}
    if user.role == User.Role.STUDENT:
        from students.models import Student
        from academics.models import Class
        student_profile, created = Student.objects.get_or_create(
            user=user,
            defaults={
                'admission_number': user.username,
                'admission_date': timezone.now().date(),
                'date_of_birth': timezone.now().date(),
                'gender': 'O',
                'address': 'Not Provided',
            }
        )
        context['classes'] = Class.objects.all()
        context['student_profile'] = student_profile
        
    return render(request, 'core/profile.html', context)

@login_required
def settings(request):
    return render(request, 'core/settings.html')

@login_required
@user_passes_test(is_admin)
def user_create(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully.')
            return redirect('user_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/user_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('user_list')
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'core/user_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('user_list')
    return render(request, 'core/user_confirm_delete.html', {'object': user})
