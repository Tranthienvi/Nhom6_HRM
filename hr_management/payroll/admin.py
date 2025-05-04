from django.contrib import admin
from .models import (
    PayrollTemplate, PayrollTemplateItem, PayrollPeriod,
    PayrollData, PayrollDataDetail, Payroll, PayrollDetail,
    PayrollPayment, PayrollPaymentDetail, Payslip
)

@admin.register(PayrollTemplate)
class PayrollTemplateAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'is_active', 'created_at')
    search_fields = ('code', 'name')
    list_filter = ('is_active',)

@admin.register(PayrollTemplateItem)
class PayrollTemplateItemAdmin(admin.ModelAdmin):
    list_display = ('template', 'code', 'name', 'item_type', 'calculation_type', 'order', 'is_active')
    search_fields = ('code', 'name')
    list_filter = ('item_type', 'calculation_type', 'is_active')

@admin.register(PayrollPeriod)
class PayrollPeriodAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'start_date', 'end_date', 'payment_date', 'status')
    search_fields = ('code', 'name')
    list_filter = ('status',)

@admin.register(PayrollData)
class PayrollDataAdmin(admin.ModelAdmin):
    list_display = ('period', 'department', 'status', 'submitted_by', 'submitted_at', 'approved_by', 'approved_at')
    search_fields = ('period__name', 'department__name')
    list_filter = ('status',)

@admin.register(PayrollDataDetail)
class PayrollDataDetailAdmin(admin.ModelAdmin):
    list_display = ('payroll_data', 'employee', 'working_days', 'overtime_hours', 'basic_salary')
    search_fields = ('employee__full_name',)

@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'period', 'status', 'created_by', 'created_at', 'approved_by', 'approved_at')
    search_fields = ('code', 'name')
    list_filter = ('status',)

@admin.register(PayrollDetail)
class PayrollDetailAdmin(admin.ModelAdmin):
    list_display = ('payroll', 'employee', 'working_days', 'basic_salary', 'gross_salary', 'net_salary')
    search_fields = ('employee__full_name',)

@admin.register(PayrollPayment)
class PayrollPaymentAdmin(admin.ModelAdmin):
    list_display = ('code', 'payroll', 'payment_date', 'payment_method', 'total_amount', 'paid_amount', 'status')
    search_fields = ('code', 'payroll__name')
    list_filter = ('status', 'payment_method')

@admin.register(PayrollPaymentDetail)
class PayrollPaymentDetailAdmin(admin.ModelAdmin):
    list_display = ('payment', 'employee', 'amount', 'status', 'payment_date')
    search_fields = ('employee__full_name',)
    list_filter = ('status',)

@admin.register(Payslip)
class PayslipAdmin(admin.ModelAdmin):
    list_display = ('code', 'payroll_detail', 'issue_date', 'is_sent', 'sent_date', 'is_viewed', 'viewed_date')
    search_fields = ('code', 'payroll_detail__employee__full_name')
    list_filter = ('is_sent', 'is_viewed')
