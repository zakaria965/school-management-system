from django.contrib import admin
from .models import User, StudentProfile, TeacherProfile, ParentProfile

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active']
    list_filter = ['role', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'user', 'class_section', 'admission_date']
    search_fields = ['student_id', 'user__first_name', 'user__last_name']
    list_filter = ['class_section']

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'user', 'designation', 'department']
    search_fields = ['employee_id', 'user__first_name', 'user__last_name', 'department']

@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'occupation']
    filter_horizontal = ['children']