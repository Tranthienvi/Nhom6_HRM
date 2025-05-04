from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import WorkShift, AttendanceSheet, AttendanceRecord
from employees.models import Employee, Position
from .forms import WorkShiftForm, AttendanceSheetForm, AttendanceRecordForm


@login_required
def attendance_dashboard(request):
	attendance_sheets = AttendanceSheet.objects.all().order_by('-created_at')[:5]
	return render(request, 'attendance/dashboard.html', {'attendance_sheets': attendance_sheets})


@login_required
def work_shift_list(request):
	work_shifts = WorkShift.objects.all()
	return render(request, 'attendance/work_shift_list.html', {'work_shifts': work_shifts})


@login_required
def work_shift_create(request):
	if request.method == 'POST':
		form = WorkShiftForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Ca làm việc đã được tạo thành công.')
			return redirect('work_shift_list')
	else:
		form = WorkShiftForm()

	return render(request, 'attendance/work_shift_form.html', {'form': form})


@login_required
def attendance_sheet_list(request):
	position_filter = request.GET.get('position')
	attendance_sheets = AttendanceSheet.objects.all().order_by('-year', '-month')

	if position_filter:
		attendance_sheets = attendance_sheets.filter(positions__id=position_filter)

	positions = Position.objects.all()

	return render(request, 'attendance/attendance_sheet_list.html', {
		'attendance_sheets': attendance_sheets,
		'positions': positions,
		'position_filter': position_filter
	})


@login_required
def attendance_sheet_create(request):
	if request.method == 'POST':
		form = AttendanceSheetForm(request.POST)
		if form.is_valid():
			attendance_sheet = form.save()
			messages.success(request, 'Bảng chấm công đã được tạo thành công.')
			return redirect('attendance_sheet_detail', pk=attendance_sheet.pk)
	else:
		form = AttendanceSheetForm()

	return render(request, 'attendance/attendance_sheet_form.html', {'form': form})


@login_required
def attendance_sheet_detail(request, pk):
	attendance_sheet = get_object_or_404(AttendanceSheet, pk=pk)
	employees = Employee.objects.filter(position__in=attendance_sheet.positions.all(), is_active=True)
	records = AttendanceRecord.objects.filter(sheet=attendance_sheet)

	return render(request, 'attendance/attendance_sheet_detail.html', {
		'attendance_sheet': attendance_sheet,
		'employees': employees,
		'records': records
	})


@login_required
def attendance_record_create(request, sheet_id, employee_id):
	attendance_sheet = get_object_or_404(AttendanceSheet, pk=sheet_id)
	employee = get_object_or_404(Employee, pk=employee_id)

	if request.method == 'POST':
		form = AttendanceRecordForm(request.POST)
		if form.is_valid():
			record = form.save(commit=False)
			record.sheet = attendance_sheet
			record.employee = employee
			record.save()
			messages.success(request, 'Bản ghi chấm công đã được tạo thành công.')
			return redirect('attendance_sheet_detail', pk=sheet_id)
	else:
		form = AttendanceRecordForm()

	return render(request, 'attendance/attendance_record_form.html', {
		'form': form,
		'attendance_sheet': attendance_sheet,
		'employee': employee
	})
