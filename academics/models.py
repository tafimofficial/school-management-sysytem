from django.db import models
from core.models import User

class AcademicYear(models.Model):
    name = models.CharField(max_length=100) # e.g. 2023-2024
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Class(models.Model):
    name = models.CharField(max_length=50) # e.g. Class 1, Grade 10
    numeric_value = models.IntegerField(unique=True) # For sorting
    
    class Meta:
        verbose_name_plural = "Classes"
        ordering = ['numeric_value']

    def __str__(self):
        return self.name

class Section(models.Model):
    name = models.CharField(max_length=10) # e.g. A, B, C
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='sections')
    class_teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'TEACHER'})
    
    class Meta:
        unique_together = ['name', 'class_name']
        ordering = ['name']

    def __str__(self):
        return f"{self.class_name.name} - {self.name}"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    classes = models.ManyToManyField(Class, related_name='subjects')
    is_elective = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.code})"

class TeacherSubjectAssignment(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'TEACHER'})
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['teacher', 'subject', 'section', 'academic_year']

    def __str__(self):
        return f"{self.teacher} - {self.subject} ({self.section})"
