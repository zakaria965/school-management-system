from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import FeeType, FeeStructure, FeePayment, Expense
from accounts.models import StudentProfile
from academics.models import ClassLevel


@login_required
def finance_dashboard(request):
    return render(request, 'finance/dashboard.html')


class FeeTypeCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = FeeType
    fields = ['name', 'description', 'is_recurring']
    template_name = 'finance/form.html'
    success_url = reverse_lazy('fee-type-list')
    
    def test_func(self):
        return self.request.user.is_admin


class FeeTypeListView(LoginRequiredMixin, ListView):
    model = FeeType
    template_name = 'finance/fee_type_list.html'
    context_object_name = 'fee_types'


class FeeStructureCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = FeeStructure
    fields = ['fee_type', 'class_level', 'amount', 'due_date', 'academic_year', 'description']
    template_name = 'finance/form.html'
    success_url = reverse_lazy('fee-structure-list')
    
    def test_func(self):
        return self.request.user.is_admin


class FeeStructureListView(LoginRequiredMixin, ListView):
    model = FeeStructure
    template_name = 'finance/fee_structure_list.html'
    context_object_name = 'fee_structures'
    
    def get_queryset(self):
        return FeeStructure.objects.select_related('fee_type', 'class_level', 'academic_year').all()


class FeePaymentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = FeePayment
    fields = ['student', 'fee_structure', 'amount_paid', 'payment_date', 'payment_method', 'transaction_id', 'status', 'remarks']
    template_name = 'finance/form.html'
    success_url = reverse_lazy('fee-payment-list')
    
    def test_func(self):
        return self.request.user.is_admin
    
    def form_valid(self, form):
        form.instance.recorded_by = self.request.user
        messages.success(self.request, 'Payment recorded')
        return super().form_valid(form)


class FeePaymentListView(LoginRequiredMixin, ListView):
    model = FeePayment
    template_name = 'finance/fee_payment_list.html'
    context_object_name = 'payments'
    
    def get_queryset(self):
        qs = FeePayment.objects.select_related('student__user', 'fee_structure__fee_type', 'fee_structure__class_level').all()
        if self.request.user.is_student:
            qs = qs.filter(student=self.request.user.student_profile)
        return qs


class ExpenseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Expense
    fields = ['title', 'category', 'amount', 'date', 'description']
    template_name = 'finance/form.html'
    success_url = reverse_lazy('expense-list')
    
    def test_func(self):
        return self.request.user.is_admin
    
    def form_valid(self, form):
        form.instance.recorded_by = self.request.user
        messages.success(self.request, 'Expense recorded')
        return super().form_valid(form)


class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = 'finance/expense_list.html'
    context_object_name = 'expenses'


@login_required
def finance_report(request):
    total_income = sum(p.amount_paid for p in FeePayment.objects.filter(status='paid'))
    total_expense = sum(e.amount for e in Expense.objects.all())
    
    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': total_income - total_expense,
    }
    return render(request, 'finance/report.html', context)