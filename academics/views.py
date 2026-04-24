from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import AcademicYear, ClassLevel, ClassSection, Subject, Timetable, Assignment, AssignmentSubmission


@login_required
def academics_dashboard(request):
    return render(request, 'academics/dashboard.html')


class AcademicYearCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = AcademicYear
    fields = ['name', 'start_date', 'end_date', 'is_current']
    template_name = 'academics/form.html'
    success_url = reverse_lazy('academic-year-list')
    
    def test_func(self):
        return self.request.user.is_admin
    
    def form_valid(self, form):
        if form.cleaned_data.get('is_current'):
            AcademicYear.objects.update(is_current=False)
        messages.success(self.request, 'Academic year created')
        return super().form_valid(form)


class AcademicYearListView(LoginRequiredMixin, ListView):
    model = AcademicYear
    template_name = 'academics/academic_year_list.html'
    context_object_name = 'academic_years'


class ClassLevelCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ClassLevel
    fields = ['name', 'numeric_level', 'description']
    template_name = 'academics/form.html'
    success_url = reverse_lazy('class-level-list')
    
    def test_func(self):
        return self.request.user.is_admin


class ClassLevelListView(LoginRequiredMixin, ListView):
    model = ClassLevel
    template_name = 'academics/class_level_list.html'
    context_object_name = 'class_levels'


class ClassSectionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ClassSection
    fields = ['name', 'class_level', 'academic_year', 'class_teacher', 'room_number', 'max_students']
    template_name = 'academics/form.html'
    success_url = reverse_lazy('class-section-list')
    
    def test_func(self):
        return self.request.user.is_admin


class ClassSectionListView(LoginRequiredMixin, ListView):
    model = ClassSection
    template_name = 'academics/class_section_list.html'
    context_object_name = 'class_sections'
    paginate_by = 20
    
    def get_queryset(self):
        return ClassSection.objects.select_related('class_level', 'academic_year', 'class_teacher').all()


class ClassSectionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ClassSection
    fields = ['name', 'class_level', 'academic_year', 'class_teacher', 'room_number', 'max_students']
    template_name = 'academics/form.html'
    success_url = reverse_lazy('class-section-list')
    
    def test_func(self):
        return self.request.user.is_admin


class ClassSectionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ClassSection
    template_name = 'academics/confirm_delete.html'
    success_url = reverse_lazy('class-section-list')
    
    def test_func(self):
        return self.request.user.is_admin


class SubjectCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Subject
    fields = ['name', 'code', 'class_level', 'teacher', 'is_elective', 'credits', 'description']
    template_name = 'academics/form.html'
    success_url = reverse_lazy('subject-list')
    
    def test_func(self):
        return self.request.user.is_admin or self.request.user.is_teacher


class SubjectListView(LoginRequiredMixin, ListView):
    model = Subject
    template_name = 'academics/subject_list.html'
    context_object_name = 'subjects'
    
    def get_queryset(self):
        return Subject.objects.select_related('class_level', 'teacher').all()


class TimetableCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Timetable
    fields = ['class_section', 'subject', 'teacher', 'day', 'start_time', 'end_time', 'room']
    template_name = 'academics/form.html'
    success_url = reverse_lazy('timetable-list')
    
    def test_func(self):
        return self.request.user.is_admin or self.request.user.is_teacher


class TimetableListView(LoginRequiredMixin, ListView):
    model = Timetable
    template_name = 'academics/timetable_list.html'
    context_object_name = 'timetables'
    
    def get_queryset(self):
        return Timetable.objects.select_related('class_section', 'subject', 'teacher').all()


class AssignmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Assignment
    fields = ['title', 'description', 'subject', 'class_section', 'due_date', 'total_marks', 'attachment', 'is_published']
    template_name = 'academics/form.html'
    success_url = reverse_lazy('assignment-list')
    
    def test_func(self):
        return self.request.user.is_admin or self.request.user.is_teacher
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Assignment created')
        return super().form_valid(form)


class AssignmentListView(LoginRequiredMixin, ListView):
    model = Assignment
    template_name = 'academics/assignment_list.html'
    context_object_name = 'assignments'
    
    def get_queryset(self):
        qs = Assignment.objects.select_related('subject', 'class_section', 'created_by').all()
        if self.request.user.is_student:
            student = self.request.user.student_profile
            qs = qs.filter(class_section=student.class_section, is_published=True)
        return qs


class AssignmentDetailView(LoginRequiredMixin, DetailView):
    model = Assignment
    template_name = 'academics/assignment_detail.html'
    context_object_name = 'assignment'


class AssignmentSubmitView(LoginRequiredMixin, CreateView):
    model = AssignmentSubmission
    fields = ['content', 'attachment']
    template_name = 'academics/assignment_submit.html'
    
    def get_success_url(self):
        return reverse_lazy('assignment-detail', kwargs={'pk': self.kwargs['pk']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assignment'] = Assignment.objects.get(pk=self.kwargs['pk'])
        return context
    
    def form_valid(self, form):
        assignment = Assignment.objects.get(pk=self.kwargs['pk'])
        student = self.request.user.student_profile
        submission, created = AssignmentSubmission.objects.get_or_create(
            assignment=assignment,
            student=student,
            defaults={'content': form.cleaned_data['content'], 'attachment': form.cleaned_data.get('attachment')}
        )
        if not created:
            submission.content = form.cleaned_data['content']
            submission.attachment = form.cleaned_data.get('attachment')
            submission.save()
        messages.success(self.request, 'Assignment submitted successfully')
        return super().form_valid(form)