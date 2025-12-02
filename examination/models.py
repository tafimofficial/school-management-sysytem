from django.db import models
from core.models import User
from students.models import Student
from academics.models import AcademicYear, Class, Section, Subject

class Exam(models.Model):
    name = models.CharField(max_length=100)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    exam_class = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Class')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.academic_year})"

class ExamSchedule(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='schedules')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_marks = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)

    class Meta:
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.exam} - {self.subject} ({self.exam_class})"

class Result(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    max_marks = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    remarks = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['exam', 'student', 'subject']

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.marks_obtained}"
