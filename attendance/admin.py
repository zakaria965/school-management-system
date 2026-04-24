from django.contrib import admin
from .models import Attendance, TeacherAttendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'date', 'status', 'marked_by']
    list_filter = ['date', 'status']
    search_fields = ['student__student_id', 'student__user__first_name']

@admin.register(TeacherAttendance)
class TeacherAttendanceAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'date', 'status']
    list_filter = ['date', 'status']
    search_fields = ['teacher__employee_id', 'teacher__user__first_name']