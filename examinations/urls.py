from django.urls import path
from . import views

urlpatterns = [
    path('', views.examinations_dashboard, name='examinations-dashboard'),
    path('types/', views.ExamTypeListView.as_view(), name='exam-type-list'),
    path('types/create/', views.ExamTypeCreateView.as_view(), name='exam-type-create'),
    path('schedules/', views.ExamScheduleListView.as_view(), name='exam-schedule-list'),
    path('schedules/create/', views.ExamScheduleCreateView.as_view(), name='exam-schedule-create'),
    path('grades/', views.GradeListView.as_view(), name='grade-list'),
    path('grades/create/', views.GradeCreateView.as_view(), name='grade-create'),
    path('grades/<int:pk>/update/', views.GradeUpdateView.as_view(), name='grade-update'),
    path('report/', views.grade_report, name='grade-report'),
]