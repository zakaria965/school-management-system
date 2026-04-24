from django.contrib import admin
from .models import ExamType, ExamSchedule, Grade

@admin.register(ExamType)
class ExamTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'weight_percentage']

@admin.register(ExamSchedule)
class ExamScheduleAdmin(admin.ModelAdmin):
    list_display = ['exam_type', 'subject', 'class_section', 'date', 'total_marks']
    list_filter = ['exam_type', 'date', 'class_section']
    search_fields = ['subject__name']

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'marks_obtained', 'grade', 'recorded_by']
    list_filter = ['exam', 'grade']
    search_fields = ['student__student_id']