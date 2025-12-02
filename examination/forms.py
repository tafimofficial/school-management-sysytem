from django import forms
from .models import Exam, ExamSchedule, Result
from academics.models import Class, Subject

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['name', 'academic_year', 'exam_class', 'section', 'start_date', 'end_date', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'academic_year': forms.Select(attrs={'class': 'form-select'}),
            'exam_class': forms.Select(attrs={'class': 'form-select'}),
            'section': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ExamScheduleForm(forms.ModelForm):
    class Meta:
        model = ExamSchedule
        fields = ['exam', 'subject', 'exam_class', 'date', 'start_time', 'end_time', 'max_marks']
        widgets = {
            'exam': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'exam_class': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'max_marks': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['marks_obtained', 'remarks']
        widgets = {
            'marks_obtained': forms.NumberInput(attrs={'class': 'form-control'}),
            'remarks': forms.TextInput(attrs={'class': 'form-control'}),
        }

ExamScheduleFormSet = forms.inlineformset_factory(
    Exam, ExamSchedule, form=ExamScheduleForm,
    extra=1, can_delete=True
)
