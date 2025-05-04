from django import forms
from .models import WorkShift, AttendanceSheet, AttendanceRecord
from employees.models import Position


class WorkShiftForm(forms.ModelForm):
	class Meta:
		model = WorkShift
		fields = ['name', 'start_time', 'end_time', 'break_time']
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
		fields = ['name', 'month', 'year', 'positions']


class AttendanceRecordForm(forms.ModelForm):
	class Meta:
		model = AttendanceRecord
		fields = ['date', 'status', 'check_in', 'check_out', 'working_hours', 'note']
		widgets = {
			'date': forms.DateInput(attrs={'type': 'date'}),
			'check_in': forms.TimeInput(attrs={'type': 'time'}),
			'check_out': forms.TimeInput(attrs={'type': 'time'}),
		}
