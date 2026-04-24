from django.urls import path
from . import views

urlpatterns = [
    path('', views.academics_dashboard, name='academics-dashboard'),
    
    # Academic Years
    path('academic-years/', views.AcademicYearListView.as_view(), name='academic-year-list'),
    path('academic-years/create/', views.AcademicYearCreateView.as_view(), name='academic-year-create'),
    
    # Class Levels
    path('class-levels/', views.ClassLevelListView.as_view(), name='class-level-list'),
    path('class-levels/create/', views.ClassLevelCreateView.as_view(), name='class-level-create'),
    
    # Class Sections
    path('class-sections/', views.ClassSectionListView.as_view(), name='class-section-list'),
    path('class-sections/create/', views.ClassSectionCreateView.as_view(), name='class-section-create'),
    path('class-sections/<int:pk>/update/', views.ClassSectionUpdateView.as_view(), name='class-section-update'),
    path('class-sections/<int:pk>/delete/', views.ClassSectionDeleteView.as_view(), name='class-section-delete'),
    
    # Subjects
    path('subjects/', views.SubjectListView.as_view(), name='subject-list'),
    path('subjects/create/', views.SubjectCreateView.as_view(), name='subject-create'),
    
    # Timetable
    path('timetables/', views.TimetableListView.as_view(), name='timetable-list'),
    path('timetables/create/', views.TimetableCreateView.as_view(), name='timetable-create'),
    
    # Assignments
    path('assignments/', views.AssignmentListView.as_view(), name='assignment-list'),
    path('assignments/create/', views.AssignmentCreateView.as_view(), name='assignment-create'),
    path('assignments/<int:pk>/', views.AssignmentDetailView.as_view(), name='assignment-detail'),
    path('assignments/<int:pk>/submit/', views.AssignmentSubmitView.as_view(), name='assignment-submit'),
]