from django.db import models
from django.conf import settings


class ExamType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    weight_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return self.name


class ExamSchedule(models.Model):
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE, related_name='schedules')
    subject = models.ForeignKey('academics.Subject', on_delete=models.CASCADE, related_name='exams')
    class_section = models.ForeignKey('academics.ClassSection', on_delete=models.CASCADE, related_name='exams')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=20, blank=True)
    total_marks = models.IntegerField(default=100)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['date', 'start_time']
    
    def __str__(self):
        return f"{self.exam_type.name} - {self.subject.name} - {self.class_section.name}"


class Grade(models.Model):
    GRADE_CHOICES = [
        ('A+', 'A+'), ('A', 'A'), ('A-', 'A-'),
        ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'),
        ('C+', 'C+'), ('C', 'C'), ('C-', 'C-'),
        ('D+', 'D+'), ('D', 'D'), ('F', 'F'),
    ]
    
    student = models.ForeignKey('accounts.StudentProfile', on_delete=models.CASCADE, related_name='grades')
    exam = models.ForeignKey(ExamSchedule, on_delete=models.CASCADE, related_name='grades')
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, blank=True)
    remarks = models.TextField(blank=True)
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'exam']
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.exam.subject.name} - {self.marks_obtained}"
    
    def save(self, *args, **kwargs):
        percentage = (self.marks_obtained / self.exam.total_marks) * 100
        if percentage >= 90:
            self.grade = 'A+'
        elif percentage >= 85:
            self.grade = 'A'
        elif percentage >= 80:
            self.grade = 'A-'
        elif percentage >= 75:
            self.grade = 'B+'
        elif percentage >= 70:
            self.grade = 'B'
        elif percentage >= 65:
            self.grade = 'B-'
        elif percentage >= 60:
            self.grade = 'C+'
        elif percentage >= 55:
            self.grade = 'C'
        elif percentage >= 50:
            self.grade = 'C-'
        elif percentage >= 45:
            self.grade = 'D+'
        elif percentage >= 40:
            self.grade = 'D'
        else:
            self.grade = 'F'
        super().save(*args, **kwargs)