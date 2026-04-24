import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import StudentProfile, TeacherProfile, ParentProfile
from academics.models import AcademicYear, ClassLevel, ClassSection, Subject, Timetable, Assignment
from attendance.models import Attendance
from examinations.models import ExamType, ExamSchedule, Grade
from finance.models import FeeType, FeeStructure, FeePayment, Expense
from communications.models import Announcement, Message
from datetime import date

User = get_user_model()

# Create Academic Year
academic_year, _ = AcademicYear.objects.get_or_create(
    name='2025-2026',
    defaults={
        'start_date': date(2025, 1, 1),
        'end_date': date(2026, 12, 31),
        'is_current': True
    }
)

# Create Class Levels
levels = []
for i in range(1, 13):
    level, _ = ClassLevel.objects.get_or_create(
        numeric_level=i,
        defaults={'name': f'Class {i}', 'description': f'Standard {i}'}
    )
    levels.append(level)

# Create Admin User
admin_user, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@school.com',
        'first_name': 'System',
        'last_name': 'Administrator',
        'role': 'admin',
        'is_staff': True,
        'is_superuser': True
    }
)
if created:
    admin_user.set_password('admin123')
    admin_user.save()

# Create Teachers
teacher_data = [
    {'username': 'teacher1', 'first_name': 'John', 'last_name': 'Smith', 'subject': 'Mathematics'},
    {'username': 'teacher2', 'first_name': 'Sarah', 'last_name': 'Johnson', 'subject': 'English'},
    {'username': 'teacher3', 'first_name': 'Michael', 'last_name': 'Brown', 'subject': 'Physics'},
    {'username': 'teacher4', 'first_name': 'Emily', 'last_name': 'Davis', 'subject': 'Chemistry'},
    {'username': 'teacher5', 'first_name': 'David', 'last_name': 'Wilson', 'subject': 'Biology'},
]

teachers = []
for t in teacher_data:
    user, created = User.objects.get_or_create(
        username=t['username'],
        defaults={
            'email': f"{t['username']}@school.com",
            'first_name': t['first_name'],
            'last_name': t['last_name'],
            'role': 'teacher'
        }
    )
    if created:
        user.set_password('password123')
        user.save()
    
    profile, _ = TeacherProfile.objects.get_or_create(
        user=user,
        defaults={
            'employee_id': f'TEACH{User.objects.filter(role="teacher").count() + 1:03d}',
            'designation': 'Teacher',
            'qualification': 'Masters Degree',
            'department': t['subject'],
            'joining_date': date(2025, 1, 1)
        }
    )
    teachers.append(profile)

# Create Students
for i in range(1, 31):
    user, created = User.objects.get_or_create(
        username=f'student{i}',
        defaults={
            'email': f'student{i}@school.com',
            'first_name': f'Student',
            'last_name': f'Name {i}',
            'role': 'student'
        }
    )
    if created:
        user.set_password('password123')
        user.save()
    
    StudentProfile.objects.get_or_create(
        user=user,
        defaults={
            'student_id': f'STU{2025}{i:04d}',
            'class_section': None,
            'admission_date': date(2025, 1, 1),
            'blood_group': ['A+', 'A-', 'B+', 'B-', 'O+', 'O-'][i % 6],
            'emergency_contact': f'555-000{i:02d}'
        }
    )

# Create Parents
for i in range(1, 11):
    user, created = User.objects.get_or_create(
        username=f'parent{i}',
        defaults={
            'email': f'parent{i}@school.com',
            'first_name': f'Parent',
            'last_name': f'Name {i}',
            'role': 'parent'
        }
    )
    if created:
        user.set_password('password123')
        user.save()
    
    ParentProfile.objects.get_or_create(
        user=user,
        defaults={'occupation': 'Business'}
    )

# Create Exam Types
exam_types = ['Mid Term', 'Final', 'Quiz', 'Assignment', 'Project']
for et in exam_types:
    ExamType.objects.get_or_create(
        name=et,
        defaults={'weight_percentage': 20.0}
    )

# Create Fee Types
fee_types = ['Tuition', 'Books', 'Transport', 'Uniform', 'Exam Fee']
for ft in fee_types:
    FeeType.objects.get_or_create(
        name=ft,
        defaults={'is_recurring': True}
    )

# Create Announcements
Announcement.objects.get_or_create(
    title='Welcome to New Academic Year',
    defaults={
        'content': 'We welcome all students and parents to the new academic year 2025-2026.',
        'author': admin_user,
        'priority': 'high',
        'is_published': True
    }
)

print("Sample data created!")
print("Admin: admin / admin123")
print("Teacher: teacher1 / password123")
print("Student: student1 / password123")