from django.db import models
from django.conf import settings


class AcademicYear(models.Model):
    name = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name


class ClassLevel(models.Model):
    name = models.CharField(max_length=50)
    numeric_level = models.IntegerField()
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['numeric_level']
    
    def __str__(self):
        return self.name


class ClassSection(models.Model):
    name = models.CharField(max_length=20)
    class_level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE, related_name='sections')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='sections')
    class_teacher = models.ForeignKey('accounts.TeacherProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_classes')
    room_number = models.CharField(max_length=20, blank=True)
    max_students = models.IntegerField(default=40)
    
    class Meta:
        unique_together = ['name', 'class_level', 'academic_year']
    
    def __str__(self):
        return f"{self.class_level.name} - {self.name}"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    class_level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE, related_name='subjects')
    teacher = models.ForeignKey('accounts.TeacherProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='subjects')
    is_elective = models.BooleanField(default=False)
    credits = models.IntegerField(default=1)
    description = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['code', 'class_level']
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class Timetable(models.Model):
    DAY_CHOICES = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]
    
    class_section = models.ForeignKey(ClassSection, on_delete=models.CASCADE, related_name='timetables')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey('accounts.TeacherProfile', on_delete=models.SET_NULL, null=True, blank=True)
    day = models.CharField(max_length=20, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=20, blank=True)
    
    class Meta:
        ordering = ['day', 'start_time']
        unique_together = ['class_section', 'day', 'start_time']
    
    def __str__(self):
        return f"{self.class_section.name} - {self.subject.name} - {self.day}"


class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assignments')
    class_section = models.ForeignKey(ClassSection, on_delete=models.CASCADE, related_name='assignments')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    total_marks = models.IntegerField(default=100)
    attachment = models.FileField(upload_to='assignments/', blank=True, null=True)
    is_published = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey('accounts.StudentProfile', on_delete=models.CASCADE, related_name='submissions')
    submitted_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True)
    attachment = models.FileField(upload_to='submissions/', blank=True, null=True)
    marks_obtained = models.IntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['assignment', 'student']
    
    def __str__(self):
        return f"{self.student.student_id} - {self.assignment.title}"