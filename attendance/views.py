from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils import timezone
from .models import Attendance, TeacherAttendance
from accounts.models import StudentProfile, TeacherProfile
from academics.models import ClassSection


@login_required
def attendance_dashboard(request):
    return render(request, 'attendance/dashboard.html')


class AttendanceMarkView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Attendance
    fields = ['student', 'date', 'status', 'remarks']
    template_name = 'attendance/mark_form.html'
    success_url = reverse_lazy('attendance-mark')
    
    def test_func(self):
        return self.request.user.is_admin or self.request.user.is_teacher
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        class_section_id = self.request.GET.get('class_section')
        if class_section_id:
            context['students'] = StudentProfile.objects.filter(class_section_id=class_section_id).select_related('user')
        context['class_sections'] = ClassSection.objects.all()
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Attendance marked successfully')
        return super().form_valid(form)


@login_required
def mark_bulk_attendance(request):
    if request.method == 'POST':
        class_section_id = request.POST.get('class_section')
        date = request.POST.get('date')
        attendance_data = request.POST.dict()
        
        students = StudentProfile.objects.filter(class_section_id=class_section_id)
        for student in students:
            status = attendance_data.get(f'status_{student.pk}', 'present')
            Attendance.objects.update_or_create(
                student=student,
                date=date,
                defaults={'status': status, 'marked_by': request.user}
            )
        messages.success(request, 'Bulk attendance marked successfully')
        return redirect('attendance-mark')
    
    class_sections = ClassSection.objects.all()
    return render(request, 'attendance/bulk_mark.html', {'class_sections': class_sections})


class AttendanceListView(LoginRequiredMixin, ListView):
    model = Attendance
    template_name = 'attendance/attendance_list.html'
    context_object_name = 'attendances'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Attendance.objects.select_related('student__user').all()
        student_id = self.request.GET.get('student')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
        
        if self.request.user.is_student:
            try:
                queryset = queryset.filter(student=self.request.user.student_profile)
            except StudentProfile.DoesNotExist:
                queryset = Attendance.objects.none()
        
        return queryset.order_by('-date')


class TeacherAttendanceCreateView(LoginRequiredMixin, CreateView):
    model = TeacherAttendance
    fields = ['teacher', 'date', 'status', 'remarks']
    template_name = 'attendance/teacher_form.html'
    success_url = reverse_lazy('teacher-attendance-list')
    
    def test_func(self):
        return self.request.user.is_admin
    
    def form_valid(self, form):
        messages.success(self.request, 'Teacher attendance marked')
        return super().form_valid(form)


class TeacherAttendanceListView(LoginRequiredMixin, ListView):
    model = TeacherAttendance
    template_name = 'attendance/teacher_attendance_list.html'
    context_object_name = 'attendances'


@login_required
def attendance_report(request):
    if request.user.is_student:
        try:
            attendances = Attendance.objects.filter(student=request.user.student_profile)
        except StudentProfile.DoesNotExist:
            attendances = Attendance.objects.none()
    else:
        attendances = Attendance.objects.select_related('student__user').all()
    
    total = attendances.count()
    present = attendances.filter(status='present').count()
    absent = attendances.filter(status='absent').count()
    late = attendances.filter(status='late').count()
    
    context = {
        'total': total,
        'present': present,
        'absent': absent,
        'late': late,
        'attendance_percentage': round((present / total * 100), 2) if total > 0 else 0,
        'attendances': attendances[:50]
    }
    return render(request, 'attendance/report.html', context)