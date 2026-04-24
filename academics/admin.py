from django.contrib import admin
from .models import (
    AcademicYear, ClassLevel, ClassSection, Subject, 
    Timetable, Assignment, AssignmentSubmission
)

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current']

@admin.register(ClassLevel)
class ClassLevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'numeric_level']
    ordering = ['numeric_level']

@admin.register(ClassSection)
class ClassSectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'class_level', 'academic_year', 'class_teacher']
    list_filter = ['class_level', 'academic_year']
    search_fields = ['name']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'class_level', 'teacher']
    list_filter = ['class_level', 'is_elective']
    search_fields = ['name', 'code']

@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ['class_section', 'subject', 'day', 'start_time', 'end_time']
    list_filter = ['day', 'class_section']
    search_fields = ['subject__name']

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'class_section', 'due_date', 'is_published']
    list_filter = ['is_published', 'class_section']
    search_fields = ['title']

@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ['assignment', 'student', 'submitted_at', 'marks_obtained']
    list_filter = ['assignment']
    search_fields = ['student__student_id']