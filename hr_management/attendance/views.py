from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import WorkShift, AttendanceSheet, AttendanceRecord
from employees.models import Employee, Position
from .forms import WorkShiftForm, AttendanceSheetForm, AttendanceRecordForm
from .models import PayrollComponent, PayrollTemplate  # Giả sử bạn có model PayrollComponent và PayrollTemplate
from .forms import PayrollComponentForm
from .forms import PayrollTemplateForm


def transfer_attendance_data(request, sheet_id):
	# Tìm kiếm AttendanceSheet theo sheet_id
	attendance_sheet = get_object_or_404(AttendanceSheet, pk=sheet_id)

	# Xử lý logic chuyển dữ liệu tính lương ở đây (ví dụ, chuyển dữ liệu từ bảng chấm công vào bảng tính lương)
	# Giả sử bạn sẽ làm một số xử lý dữ liệu ở đây, ví dụ:
	# attendance_sheet.calculate_salary()

	return render(request, 'attendance/transfer_attendance_data.html', {'attendance_sheet': attendance_sheet})

def payroll_detail(request, pk):
	# Tìm kiếm PayrollTemplate theo pk
	payroll_template = get_object_or_404(PayrollTemplate, pk=pk)

	return render(request, 'attendance/payroll_detail.html', {'payroll_template': payroll_template})

def payroll_create(request):
    if request.method == 'POST':
        form = PayrollTemplateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendance:payroll_list')  # Sau khi lưu xong, chuyển hướng về danh sách bảng lương
    else:
        form = PayrollTemplateForm()

    return render(request, 'attendance/payroll_create.html', {'form': form})

def payroll_list(request):
    # Lấy tất cả các mẫu bảng lương
    payroll_templates = PayrollTemplate.objects.all()
    return render(request, 'attendance/payroll_list.html', {'payroll_templates': payroll_templates})

def payroll_component_create(request, template_id):
    # Lấy mẫu bảng lương theo template_id
    payroll_template = get_object_or_404(PayrollTemplate, pk=template_id)

    if request.method == 'POST':
        form = PayrollComponentForm(request.POST)
        if form.is_valid():
            # Lưu thành phần bảng lương mới với liên kết tới payroll_template
            payroll_component = form.save(commit=False)
            payroll_component.payroll_template = payroll_template
            payroll_component.save()
            return redirect('payroll_template_detail', pk=template_id)
    else:
        form = PayrollComponentForm()

    return render(request, 'payroll_component_form.html', {'form': form, 'payroll_template': payroll_template})

def payroll_template_detail(request, pk):
	# Lấy đối tượng PayrollTemplate theo pk
	payroll_template = get_object_or_404(PayrollTemplate, pk=pk)

	# Trả về chi tiết mẫu bảng lương
	return render(request, 'payroll_template_detail.html', {'payroll_template': payroll_template})

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

	# Tạo từ điển để lưu trữ bản ghi chấm công theo nhân viên
	employee_records = {}
	for employee in employees:
		employee_records[employee.id] = {
			'employee': employee,
			'records': records.filter(employee=employee)
		}

	return render(request, 'attendance/attendance_sheet_detail.html', {
		'attendance_sheet': attendance_sheet,
		'employee_records': employee_records
	})


def payroll_dashboard(request):
    # Logic xử lý cho dashboard của bảng lương
    return render(request, 'payroll/dashboard.html')

def payroll_template_list(request):
    # Logic xử lý danh sách mẫu bảng lương
    return render(request, 'payroll_template_list.html')  # Chỉ định template cần render

def payroll_template_create(request):
    if request.method == 'POST':
        form = PayrollTemplateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payroll_template_list')  # Sau khi tạo thành công, chuyển hướng đến danh sách mẫu bảng lương
    else:
        form = PayrollTemplateForm()  # Nếu là GET request, tạo form mới

    return render(request, 'payroll_template_create.html', {'form': form})

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
