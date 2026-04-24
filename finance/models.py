from django.db import models
from django.conf import settings


class FeeType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_recurring = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name


class FeeStructure(models.Model):
    fee_type = models.ForeignKey(FeeType, on_delete=models.CASCADE, related_name='structures')
    class_level = models.ForeignKey('academics.ClassLevel', on_delete=models.CASCADE, related_name='fee_structures')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    academic_year = models.ForeignKey('academics.AcademicYear', on_delete=models.CASCADE, related_name='fee_structures')
    description = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['fee_type', 'class_level', 'academic_year']
    
    def __str__(self):
        return f"{self.fee_type.name} - {self.class_level.name} - {self.amount}"


class FeePayment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    
    student = models.ForeignKey('accounts.StudentProfile', on_delete=models.CASCADE, related_name='fee_payments')
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE, related_name='payments')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    remarks = models.TextField(blank=True)
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.fee_structure.fee_type.name} - {self.status}"


class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('salary', 'Salary'),
        ('infrastructure', 'Infrastructure'),
        ('supplies', 'Supplies'),
        ('utilities', 'Utilities'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True)
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.title} - {self.amount}"