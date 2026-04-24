from django.urls import path
from . import views

urlpatterns = [
    path('', views.attendance_dashboard, name='attendance-dashboard'),
    path('mark/', views.AttendanceMarkView.as_view(), name='attendance-mark'),
    path('mark-bulk/', views.mark_bulk_attendance, name='attendance-mark-bulk'),
    path('list/', views.AttendanceListView.as_view(), name='attendance-list'),
    path('teacher/', views.TeacherAttendanceListView.as_view(), name='teacher-attendance-list'),
    path('teacher/create/', views.TeacherAttendanceCreateView.as_view(), name='teacher-attendance-create'),
    path('report/', views.attendance_report, name='attendance-report'),
]