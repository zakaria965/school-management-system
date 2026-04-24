from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('parent', 'Parent'),
    ]
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.role})"
    
    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser
    
    @property
    def is_teacher(self):
        return self.role == 'teacher'
    
    @property
    def is_student(self):
        return self.role == 'student'
    
    @property
    def is_parent(self):
        return self.role == 'parent'


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True)
    class_section = models.ForeignKey('academics.ClassSection', on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    parent = models.ForeignKey('ParentProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='linked_students')
    admission_date = models.DateField()
    blood_group = models.CharField(max_length=5, blank=True)
    emergency_contact = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f"{self.student_id} - {self.user.get_full_name()}"


class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    designation = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    joining_date = models.DateField()
    specializations = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name()}"


class ParentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile')
    children = models.ManyToManyField(StudentProfile, related_name='linked_parents')
    occupation = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()}"