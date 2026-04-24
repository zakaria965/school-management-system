from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.db import models
from django.db.models import Count, Q
from datetime import timedelta
from .models import User, StudentProfile, TeacherProfile, ParentProfile
from academics.models import ClassSection, Subject, AcademicYear, Assignment
from attendance.models import Attendance
from examinations.models import Grade, ExamSchedule
from finance.models import FeePayment, Expense
from communications.models import Announcement
from .forms import UserCreationForm, UserUpdateForm, StudentProfileForm, TeacherProfileForm, ParentProfileForm


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


class SignUpView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created successfully. Please login.')
        return response


@login_required
def dashboard(request):
    user = request.user
    
    # Get stats for admin
    if user.is_admin:
        total_students = User.objects.filter(role='student').count()
        total_teachers = User.objects.filter(role='teacher').count()
        total_classes = ClassSection.objects.count()
        total_sections = ClassSection.objects.count()
        
        today = timezone.now().date()
        present_today = Attendance.objects.filter(date=today, status='present').count()
        total_today = Attendance.objects.filter(date=today).count()
        attendance_rate = round((present_today / total_today * 100), 1) if total_today > 0 else 0
        
        total_income = FeePayment.objects.filter(status='paid').aggregate(sum=models.Sum('amount_paid'))['sum'] or 0
        total_expense = Expense.objects.aggregate(sum=models.Sum('amount'))['sum'] or 0
        
        stats = {
            'total_students': total_students,
            'total_teachers': total_teachers,
            'total_classes': ClassLevel.objects.count() if 'academics' in dir() else total_classes,
            'total_classes': total_classes,
            'total_sections': total_sections,
            'attendance_rate': attendance_rate,
            'present_today': present_today,
            'total_income': total_income,
            'total_expense': total_expense,
        }
        
        # Recent activities
        recent_activities = [
            {'icon': 'user-add-line', 'color': 'blue', 'title': 'New Student Admitted', 'description': 'John Doe added to Class 10-A', 'time': '2 min ago'},
            {'icon': 'file-text-line', 'color': 'purple', 'title': 'Exam Results Published', 'description': 'Mid-term results for Class 9', 'time': '1 hour ago'},
            {'icon': 'money-dollar-line', 'color': 'green', 'title': 'Fee Payment Received', 'description': '$500 from Student ID 20250001', 'time': '2 hours ago'},
            {'icon': 'calendar-check-line', 'color': 'orange', 'title': 'Attendance Marked', 'description': 'Class 10-A attendance updated', 'time': '3 hours ago'},
            {'icon': 'megaphone-line', 'color': 'blue', 'title': 'New Announcement', 'description': 'Parent-Teacher meeting schedule', 'time': '5 hours ago'},
        ]
        
        # Upcoming events
        upcoming_events = [
            {'month': 'APR', 'day': '25', 'title': 'Mid-Term Exams', 'description': 'Starting from Monday'},
            {'month': 'APR', 'day': '28', 'title': 'Parent-Teacher Meet', 'description': 'Annual PTM in auditorium'},
            {'month': 'MAY', 'day': '01', 'title': 'Labor Day', 'description': 'School Holiday'},
            {'month': 'MAY', 'day': '15', 'title': 'Sports Day', 'description': 'Annual sports event'},
        ]
        
        # Announcements
        announcements = Announcement.objects.filter(is_published=True)[:5]
        
        context = {
            'user': user,
            'stats': stats,
            'recent_activities': recent_activities,
            'upcoming_events': upcoming_events,
            'announcements': announcements,
        }
        return render(request, 'dashboard/admin.html', context)
    
    elif user.is_teacher:
        try:
            teacher = user.teacher_profile
            subjects = Subject.objects.filter(teacher=teacher)
            classes = ClassSection.objects.filter(class_teacher=teacher)
            
            context = {
                'user': user,
                'teacher': teacher,
                'subjects': subjects,
                'classes': classes,
                'total_students': sum(cs.students.count() for cs in classes),
            }
        except:
            context = {'user': user}
        return render(request, 'dashboard/teacher.html', context)
    
    elif user.is_student:
        try:
            student = user.student_profile
            assignments = Assignment.objects.filter(class_section=student.class_section, is_published=True)[:5]
            
            attendances = Attendance.objects.filter(student=student)
            total = attendances.count()
            present = attendances.filter(status='present').count()
            attendance_rate = round((present / total * 100), 1) if total > 0 else 0
            
            grades = Grade.objects.filter(student=student)
            avg_marks = grades.aggregate(avg=models.Avg('marks_obtained'))['avg'] or 0
            
            context = {
                'user': user,
                'student': student,
                'assignments': assignments,
                'attendance_rate': attendance_rate,
                'avg_marks': round(avg_marks, 1),
            }
        except:
            context = {'user': user}
        return render(request, 'dashboard/student.html', context)
    
    elif user.is_parent:
        try:
            parent = user.parent_profile
            children = parent.children.all()
            
            context = {
                'user': user,
                'children': children,
            }
        except:
            context = {'user': user}
        return render(request, 'dashboard/parent.html', context)
    
    return render(request, 'dashboard/base.html', {'user': user})


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 20
    
    def test_func(self):
        return self.request.user.is_admin
    
    def get_queryset(self):
        role = self.request.GET.get('role')
        qs = User.objects.exclude(pk=self.request.user.pk).select_related()
        if role:
            qs = qs.filter(role=role)
        return qs.order_by('-date_joined')


class UserCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('user-list')
    
    def test_func(self):
        return self.request.user.is_admin
    
    def form_valid(self, form):
        messages.success(self.request, 'User created successfully')
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('dashboard')
    
    def get_object(self):
        return self.request.user


class StudentListView(LoginRequiredMixin, ListView):
    model = StudentProfile
    template_name = 'accounts/student_list.html'
    context_object_name = 'students'
    paginate_by = 20
    
    def get_queryset(self):
        return StudentProfile.objects.select_related('user', 'class_section', 'class_section__class_level').all()


class StudentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = StudentProfile
    form_class = StudentProfileForm
    template_name = 'accounts/student_form.html'
    success_url = reverse_lazy('student-list')
    
    def test_func(self):
        return self.request.user.is_admin
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Student'
        return context


class StudentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = StudentProfile
    form_class = StudentProfileForm
    template_name = 'accounts/student_form.html'
    success_url = reverse_lazy('student-list')
    
    def test_func(self):
        return self.request.user.is_admin
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Student'
        return context


class StudentDetailView(LoginRequiredMixin, DetailView):
    model = StudentProfile
    template_name = 'accounts/student_detail.html'
    context_object_name = 'student'
    
    def get_queryset(self):
        return StudentProfile.objects.select_related('user', 'class_section', 'class_section__class_level')


class StudentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = StudentProfile
    template_name = 'accounts/student_confirm_delete.html'
    success_url = reverse_lazy('student-list')
    
    def test_func(self):
        return self.request.user.is_admin


class TeacherListView(LoginRequiredMixin, ListView):
    model = TeacherProfile
    template_name = 'accounts/teacher_list.html'
    context_object_name = 'teachers'
    paginate_by = 20
    
    def get_queryset(self):
        return TeacherProfile.objects.select_related('user').all()


class TeacherCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = TeacherProfile
    form_class = TeacherProfileForm
    template_name = 'accounts/teacher_form.html'
    success_url = reverse_lazy('teacher-list')
    
    def test_func(self):
        return self.request.user.is_admin
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Teacher'
        return context


class TeacherUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = TeacherProfile
    form_class = TeacherProfileForm
    template_name = 'accounts/teacher_form.html'
    success_url = reverse_lazy('teacher-list')
    
    def test_func(self):
        return self.request.user.is_admin
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Teacher'
        return context


class TeacherDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = TeacherProfile
    template_name = 'accounts/teacher_confirm_delete.html'
    success_url = reverse_lazy('teacher-list')
    
    def test_func(self):
        return self.request.user.is_admin


class ParentListView(LoginRequiredMixin, ListView):
    model = ParentProfile
    template_name = 'accounts/parent_list.html'
    context_object_name = 'parents'
    paginate_by = 20
    
    def get_queryset(self):
        return ParentProfile.objects.select_related('user').prefetch_related('children', 'children__user').all()