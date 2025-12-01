from django import forms
from .models import TeacherSubjectAssignment, Subject, Section, AcademicYear
from core.models import User

class TeacherAssignmentForm(forms.ModelForm):
    class Meta:
        model = TeacherSubjectAssignment
        fields = ['teacher', 'subject', 'section', 'academic_year']
        widgets = {
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'section': forms.Select(attrs={'class': 'form-control'}),
            'academic_year': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        class_id = kwargs.pop('class_id', None)
        super().__init__(*args, **kwargs)
        
        if class_id:
            self.fields['subject'].queryset = Subject.objects.filter(classes__id=class_id)
            self.fields['section'].queryset = Section.objects.filter(class_name_id=class_id)
        
        self.fields['teacher'].queryset = User.objects.filter(role='TEACHER')
        self.fields['academic_year'].queryset = AcademicYear.objects.filter(is_active=True)
