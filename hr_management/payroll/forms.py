from django import forms
from .models import PayrollTemplate, PayrollComponent, Payroll
from employees.models import Position
from attendance.models import AttendanceSheet


class PayrollTemplateForm(forms.ModelForm):
	positions = forms.ModelMultipleChoiceField(
		queryset=Position.objects.all(),
		widget=forms.CheckboxSelectMultiple,
		required=True,
		label='Vị trí áp dụng'
	)

	class Meta:
		model = PayrollTemplate
		fields = ['name', 'positions', 'is_active']


class PayrollComponentForm(forms.ModelForm):
	class Meta:
		model = PayrollComponent
		fields = ['name', 'component_type', 'value', 'formula']


class PayrollForm(forms.ModelForm):
	positions = forms.ModelMultipleChoiceField(
		queryset=Position.objects.all(),
		widget=forms.CheckboxSelectMultiple,
		required=True,
		label='Vị trí áp dụng'
	)

	class Meta:
		model = Payroll
		fields = ['name', 'month', 'year', 'positions', 'template', 'attendance_sheet']
