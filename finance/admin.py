from django.contrib import admin
from .models import FeeType, FeeStructure, FeePayment, Expense

@admin.register(FeeType)
class FeeTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_recurring']

@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ['fee_type', 'class_level', 'amount', 'due_date']
    list_filter = ['class_level', 'academic_year']

@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ['student', 'fee_structure', 'amount_paid', 'status', 'payment_date']
    list_filter = ['status', 'payment_date']
    search_fields = ['student__student_id']

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'amount', 'date']
    list_filter = ['category', 'date']
    search_fields = ['title']