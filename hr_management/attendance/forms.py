from django import forms
from .models import WorkShift, AttendanceSheet, AttendanceRecord
from employees.models import Position
from .models import Employee
from .models import PayrollTemplate
from .models import PayrollComponent

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'code', 'first_name', 'last_name', 'full_name', 'gender', 'date_of_birth', 'id_number',
            'phone', 'email', 'position', 'department', 'join_date', 'is_active', 'photo', 'labor_status',
            'employment_type', 'contract_type', 'dependents'
        ]
        widgets = {
            'join_date': forms.SelectDateWidget(years=range(2000, 2031)),
        }

class WorkShiftForm(forms.ModelForm):
	class Meta:
		model = WorkShift
		fields = [
			'name', 'start_time', 'end_time', 'break_time',
			# Các trường mới bổ sung
			'working_hours', 'normal_day_coefficient',
			'rest_day_coefficient', 'holiday_coefficient', 'is_active'
		]
		widgets = {
			'start_time': forms.TimeInput(attrs={'type': 'time'}),
			'end_time': forms.TimeInput(attrs={'type': 'time'}),
		}


class AttendanceSheetForm(forms.ModelForm):
	positions = forms.ModelMultipleChoiceField(
		queryset=Position.objects.all(),
		widget=forms.CheckboxSelectMultiple,
		required=True,
		label='Vị trí áp dụng'
	)

	class Meta:
		model = AttendanceSheet
		fields = [
			'name', 'month', 'year', 'positions',
			# Các trường mới bổ sung
			'attendance_type', 'standard_workdays',
			'paid_leave', 'approved_leave', 'unapproved_leave'
		]
		widgets = {
			'attendance_type': forms.Select(attrs={'class': 'form-select'}),
		}


class AttendanceRecordForm(forms.ModelForm):
	class Meta:
		model = AttendanceRecord
		fields = [
			'date', 'status', 'check_in', 'check_out',
			'working_hours', 'note', 'work_shift'
		]
		widgets = {
			'date': forms.DateInput(attrs={'type': 'date'}),
			'check_in': forms.TimeInput(attrs={'type': 'time'}),
			'check_out': forms.TimeInput(attrs={'type': 'time'}),
			'work_shift': forms.Select(attrs={'class': 'form-select'}),
		}
class PayrollTemplateForm(forms.ModelForm):
    class Meta:
        model = PayrollTemplate
        fields = ['name', 'salary', 'bonus', 'deductions', 'effective_date', 'is_active']

class PayrollComponentForm(forms.ModelForm):
    class Meta:
        model = PayrollComponent
        fields = ['name', 'amount', 'component_type', 'is_active']  # Các trường trong PayrollComponent