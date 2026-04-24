from django.urls import path
from . import views

urlpatterns = [
    path('', views.finance_dashboard, name='finance-dashboard'),
    path('types/', views.FeeTypeListView.as_view(), name='fee-type-list'),
    path('types/create/', views.FeeTypeCreateView.as_view(), name='fee-type-create'),
    path('structures/', views.FeeStructureListView.as_view(), name='fee-structure-list'),
    path('structures/create/', views.FeeStructureCreateView.as_view(), name='fee-structure-create'),
    path('payments/', views.FeePaymentListView.as_view(), name='fee-payment-list'),
    path('payments/create/', views.FeePaymentCreateView.as_view(), name='fee-payment-create'),
    path('expenses/', views.ExpenseListView.as_view(), name='expense-list'),
    path('expenses/create/', views.ExpenseCreateView.as_view(), name='expense-create'),
    path('report/', views.finance_report, name='finance-report'),
]