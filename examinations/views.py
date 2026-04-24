from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import ExamType, ExamSchedule, Grade
from academics.models import ClassSection, Subject


@login_required
def examinations_dashboard(request):
    return render(request, 'examinations/dashboard.html')


class ExamTypeCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ExamType
    fields = ['name', 'description', 'weight_percentage']
    template_name = 'examinations/form.html'
    success_url = reverse_lazy('exam-type-list')
    
    def test_func(self):
        return self.request.user.is_admin


class ExamTypeListView(LoginRequiredMixin, ListView):
    model = ExamType
    template_name = 'examinations/exam_type_list.html'
    context_object_name = 'exam_types'


class ExamScheduleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ExamSchedule
    fields = ['exam_type', 'subject', 'class_section', 'date', 'start_time', 'end_time', 'room', 'total_marks']
    template_name = 'examinations/form.html'
    success_url = reverse_lazy('exam-schedule-list')
    
    def test_func(self):
        return self.request.user.is_admin or self.request.user.is_teacher
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Exam scheduled')
        return super().form_valid(form)


class ExamScheduleListView(LoginRequiredMixin, ListView):
    model = ExamSchedule
    template_name = 'examinations/exam_schedule_list.html'
    context_object_name = 'exams'
    
    def get_queryset(self):
        qs = ExamSchedule.objects.select_related('exam_type', 'subject', 'class_section').all()
        class_section_id = self.request.GET.get('class_section')
        if class_section_id:
            qs = qs.filter(class_section_id=class_section_id)
        return qs


class GradeCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Grade
    fields = ['student', 'exam', 'marks_obtained', 'remarks']
    template_name = 'examinations/form.html'
    success_url = reverse_lazy('grade-list')
    
    def test_func(self):
        return self.request.user.is_admin or self.request.user.is_teacher
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exam_id = self.request.GET.get('exam')
        if exam_id:
            context['exam'] = ExamSchedule.objects.get(pk=exam_id)
            context['students'] = context['exam'].class_section.students.select_related('user')
        return context
    
    def form_valid(self, form):
        form.instance.recorded_by = self.request.user
        messages.success(self.request, 'Grade recorded')
        return super().form_valid(form)


class GradeListView(LoginRequiredMixin, ListView):
    model = Grade
    template_name = 'examinations/grade_list.html'
    context_object_name = 'grades'
    
    def get_queryset(self):
        qs = Grade.objects.select_related('student__user', 'exam__subject').all()
        if self.request.user.is_student:
            qs = qs.filter(student=self.request.user.student_profile)
        return qs


class GradeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Grade
    fields = ['marks_obtained', 'remarks']
    template_name = 'examinations/form.html'
    success_url = reverse_lazy('grade-list')
    
    def test_func(self):
        return self.request.user.is_admin or self.request.user.is_teacher


@login_required
def grade_report(request):
    if request.user.is_student:
        grades = Grade.objects.filter(student=request.user.student_profile).select_related('exam__subject')
    else:
        student_id = request.GET.get('student')
        grades = Grade.objects.select_related('student__user', 'exam__subject').all()
        if student_id:
            grades = grades.filter(student_id=student_id)
    
    context = {
        'grades': grades,
    }
    return render(request, 'examinations/grade_report.html', context)