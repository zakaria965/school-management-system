from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/create/', views.UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/update/', views.UserUpdateView.as_view(), name='user-update'),
    
    # Students CRUD
    path('students/', views.StudentListView.as_view(), name='student-list'),
    path('students/create/', views.StudentCreateView.as_view(), name='student-create'),
    path('students/<int:pk>/', views.StudentDetailView.as_view(), name='student-detail'),
    path('students/<int:pk>/update/', views.StudentUpdateView.as_view(), name='student-update'),
    path('students/<int:pk>/delete/', views.StudentDeleteView.as_view(), name='student-delete'),
    
    # Teachers CRUD
    path('teachers/', views.TeacherListView.as_view(), name='teacher-list'),
    path('teachers/create/', views.TeacherCreateView.as_view(), name='teacher-create'),
    path('teachers/<int:pk>/update/', views.TeacherUpdateView.as_view(), name='teacher-update'),
    path('teachers/<int:pk>/delete/', views.TeacherDeleteView.as_view(), name='teacher-delete'),
    
    # Parents
    path('parents/', views.ParentListView.as_view(), name='parent-list'),
]