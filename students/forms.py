from django import forms
from .models import Student, StudentGuardian
from core.models import User

class StudentForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = Student
        fields = ['admission_number', 'admission_date', 'roll_number', 'date_of_birth', 
                  'gender', 'blood_group', 'address', 'phone_number', 'current_class', 'section']
        widgets = {
            'admission_date': forms.DateInput(attrs={'type': 'date'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def save(self, commit=True):
        student = super().save(commit=False)
        if not student.pk:  # Create new user if new student
            user = User.objects.create_user(
                username=self.cleaned_data['admission_number'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password'] or 'password123', # Default password
                role=User.Role.STUDENT
            )
            student.user = user
        else:
            student.user.first_name = self.cleaned_data['first_name']
            student.user.last_name = self.cleaned_data['last_name']
            student.user.email = self.cleaned_data['email']
            if commit:
                student.user.save()
        
        if commit:
            student.save()
        return student

class StudentGuardianForm(forms.ModelForm):
    class Meta:
        model = StudentGuardian
        fields = ['name', 'relationship', 'phone_number', 'email', 'occupation']
