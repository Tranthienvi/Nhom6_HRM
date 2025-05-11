from django import forms
from .models import (
    PayrollTemplate, PayrollTemplateItem, PayrollPeriod,
    PayrollData, PayrollDataDetail, Payroll, PayrollDetail,
    PayrollPayment, PayrollPaymentDetail, Payslip
)

from employees.models import Employee

from django import forms
from .models import PayrollTemplate
from .models import PayrollPeriod

class PayrollTemplateForm(forms.ModelForm):
    class Meta:
        model = PayrollTemplate
        fields = ['name', 'salary', 'bonus', 'deductions', 'effective_date', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'bonus': forms.NumberInput(attrs={'class': 'form-control'}),
            'deductions': forms.NumberInput(attrs={'class': 'form-control'}),
            'effective_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class PayrollTemplateItemForm(forms.ModelForm):
    class Meta:
        model = PayrollTemplateItem
        fields = ['code', 'name', 'item_type', 'calculation_type', 'order', 'is_active']  # Xóa 'value'
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'item_type': forms.Select(attrs={'class': 'form-select'}),
            'calculation_type': forms.Select(attrs={'class': 'form-select'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class PayrollPeriodForm(forms.ModelForm):
    class Meta:
        model = PayrollPeriod
        fields = ['code', 'name', 'start_date', 'end_date', 'payment_date', 'status']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'payment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class PayrollDataForm(forms.ModelForm):
    class Meta:
        model = PayrollData
        fields = ['period', 'department']
        widgets = {
            'period': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
        }


class PayrollDataDetailForm(forms.ModelForm):
    class Meta:
        model = PayrollDataDetail
        fields = ['employee', 'working_days', 'overtime_hours', 'leave_days',
                 'basic_salary', 'allowance', 'bonus', 'deduction']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-select'}),
            'working_days': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'overtime_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'leave_days': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'basic_salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'allowance': forms.NumberInput(attrs={'class': 'form-control'}),
            'bonus': forms.NumberInput(attrs={'class': 'form-control'}),
            'deduction': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = ['period', 'code', 'name']
        widgets = {
            'period': forms.Select(attrs={'class': 'form-select'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PayrollDetailForm(forms.ModelForm):
    class Meta:
        model = PayrollDetail
        fields = ['employee', 'working_days', 'overtime_hours', 'leave_days',
                 'basic_salary', 'allowance', 'bonus', 'deduction',
                 'gross_salary', 'tax', 'net_salary', ]
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-select'}),
            'working_days': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'overtime_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'leave_days': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'basic_salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'allowance': forms.NumberInput(attrs={'class': 'form-control'}),
            'bonus': forms.NumberInput(attrs={'class': 'form-control'}),
            'deduction': forms.NumberInput(attrs={'class': 'form-control'}),
            'gross_salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'tax': forms.NumberInput(attrs={'class': 'form-control'}),
            'net_salary': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class PayrollPaymentForm(forms.ModelForm):
    class Meta:
        model = PayrollPayment
        fields = ['payroll', 'code', 'payment_date', 'payment_method', 'total_amount']
        widgets = {
            'payroll': forms.Select(attrs={'class': 'form-select'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'payment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class PayrollPaymentDetailForm(forms.ModelForm):
    class Meta:
        model = PayrollPaymentDetail
        fields = ['employee', 'amount', 'status', 'payment_date', 'reference']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'payment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'reference': forms.TextInput(attrs={'class': 'form-control'}),

        }

class PayslipForm(forms.ModelForm):
    class Meta:
        model = Payslip
        fields = ['code', 'issue_date']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'issue_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class PayrollFilterForm(forms.Form):
    period = forms.ModelChoiceField(
        queryset=PayrollPeriod.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    status = forms.ChoiceField(
        choices=[('', '-- Tất cả trạng thái --')] + list(PayrollPayment.STATUS_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tìm kiếm...'})
    )

class PayrollDataFilterForm(forms.Form):
    period = forms.ModelChoiceField(
        queryset=PayrollPeriod.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    status = forms.ChoiceField(
        choices=[('', '-- Tất cả --'), ('active', 'Active'), ('inactive', 'Inactive')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    status = forms.ChoiceField(
        choices=[('', '-- Tất cả trạng thái --')] + list(PayrollPayment.STATUS_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tìm kiếm...'})
    )

class PayrollPaymentFilterForm(forms.Form):
    payroll = forms.ModelChoiceField(
        queryset=Payroll.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    status = forms.ChoiceField(
        choices=[('', '-- Tất cả trạng thái --')] + list(PayrollPayment.STATUS_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    payment_method = forms.ChoiceField(
        choices=[('', '-- Tất cả phương thức --')] + list(PayrollPayment.PAYMENT_METHOD_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tìm kiếm...'})
    )
