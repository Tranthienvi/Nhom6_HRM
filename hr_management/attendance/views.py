from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import WorkShift, AttendanceSheet, AttendanceRecord
from employees.models import Employee, Position
from .forms import WorkShiftForm, AttendanceSheetForm, AttendanceRecordForm
from .models import PayrollComponent, PayrollTemplate  # Giả sử bạn có model PayrollComponent và PayrollTemplate
from .forms import PayrollComponentForm
from .forms import PayrollTemplateForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.core.paginator import Paginator
from django.utils import timezone
from django.http import HttpResponse
import csv
import datetime
from django.shortcuts import render
from .models import WorkShift, AttendanceSheet, AttendanceRecord, PayrollTemplate, PayrollComponent
from employees.models import Employee, Position, Department
from .forms import (WorkShiftForm, AttendanceSheetForm, AttendanceRecordForm,
					PayrollTemplateForm, PayrollComponentForm, AttendanceSheetFilterForm)


@login_required
def attendance_dashboard(request):
	# Thống kê tổng quan
	total_sheets = AttendanceSheet.objects.count()
	active_sheets = AttendanceSheet.objects.filter(is_locked=False).count()
	total_employees = Employee.objects.filter(is_active=True).count()

	# Bảng chấm công gần đây
	recent_sheets = AttendanceSheet.objects.all().order_by('-created_at')[:5]

	context = {
		'total_sheets': total_sheets,
		'active_sheets': active_sheets,
		'total_employees': total_employees,
		'recent_sheets': recent_sheets,
	}
	return render(request, 'attendance/dashboard.html', context)


@login_required
def attendance_sheet_list(request):
	# Lọc theo đơn vị
	filter_form = AttendanceSheetFilterForm(request.GET)
	sheets = AttendanceSheet.objects.all().order_by('-year', '-month')

	if filter_form.is_valid():
		department = filter_form.cleaned_data.get('department')
		if department:
			# Lọc các bảng chấm công có vị trí thuộc đơn vị được chọn
			positions = Position.objects.filter(department=department)
			sheets = sheets.filter(positions__in=positions).distinct()

	# Phân trang
	paginator = Paginator(sheets, 10)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	context = {
		'page_obj': page_obj,
		'filter_form': filter_form,
	}
	return render(request, 'attendance/attendance_sheet_list.html', context)


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

	context = {
		'form': form,
		'title': 'Thêm bảng chấm công',
	}
	return render(request, 'attendance/attendance_sheet_form.html', context)


@login_required
def attendance_sheet_update(request, pk):
	attendance_sheet = get_object_or_404(AttendanceSheet, pk=pk)

	if attendance_sheet.is_locked:
		messages.error(request, 'Bảng chấm công đã bị khóa, không thể chỉnh sửa.')
		return redirect('attendance_sheet_detail', pk=attendance_sheet.pk)

	if request.method == 'POST':
		form = AttendanceSheetForm(request.POST, instance=attendance_sheet)
		if form.is_valid():
			form.save()
			messages.success(request, 'Bảng chấm công đã được cập nhật thành công.')
			return redirect('attendance_sheet_detail', pk=attendance_sheet.pk)
	else:
		form = AttendanceSheetForm(instance=attendance_sheet)

	context = {
		'form': form,
		'attendance_sheet': attendance_sheet,
		'title': 'Cập nhật bảng chấm công',
	}
	return render(request, 'attendance/attendance_sheet_form.html', context)


@login_required
def attendance_sheet_detail(request, pk):
	attendance_sheet = get_object_or_404(AttendanceSheet, pk=pk)

	# Lấy tất cả bản ghi chấm công của bảng này
	attendance_records = AttendanceRecord.objects.filter(sheet=attendance_sheet).select_related('employee',
																								'work_shift')

	# Thống kê
	total_records = attendance_records.count()
	present_count = attendance_records.filter(status='present').count()
	absent_count = attendance_records.filter(status='absent').count()
	late_count = attendance_records.filter(status='late').count()
	leave_count = attendance_records.filter(status='leave').count()

	context = {
		'attendance_sheet': attendance_sheet,
		'attendance_records': attendance_records,
		'total_records': total_records,
		'present_count': present_count,
		'absent_count': absent_count,
		'late_count': late_count,
		'leave_count': leave_count,
	}
	return render(request, 'attendance/attendance_sheet_detail.html', context)


@login_required
def attendance_record_create(request, sheet_id=None, employee_id=None):
	# Nếu có sheet_id, lấy bảng chấm công tương ứng
	attendance_sheet = None
	employee = None

	if sheet_id:
		attendance_sheet = get_object_or_404(AttendanceSheet, pk=sheet_id)
		if attendance_sheet.is_locked:
			messages.error(request, 'Bảng chấm công đã bị khóa, không thể thêm dữ liệu.')
			return redirect('attendance_sheet_detail', pk=sheet_id)

	if employee_id:
		employee = get_object_or_404(Employee, pk=employee_id)

	if request.method == 'POST':
		form = AttendanceRecordForm(request.POST)
		if form.is_valid():
			record = form.save(commit=False)

			if attendance_sheet:
				record.sheet = attendance_sheet
			else:
				sheet_id = request.POST.get('sheet_id')
				if not sheet_id:
					messages.error(request, 'Vui lòng chọn bảng chấm công')
					return redirect('attendance_record_create')
				record.sheet = get_object_or_404(AttendanceSheet, pk=sheet_id)

			if employee:
				record.employee = employee
			else:
				employee_id = request.POST.get('employee_id')
				if not employee_id:
					messages.error(request, 'Vui lòng chọn nhân viên')
					return redirect('attendance_record_create')
				record.employee = get_object_or_404(Employee, pk=employee_id)

			# Kiểm tra xem đã có bản ghi cho nhân viên và ngày này chưa
			existing_record = AttendanceRecord.objects.filter(
				sheet=record.sheet,
				employee=record.employee,
				date=record.date
			).first()

			if existing_record:
				messages.error(request,
							   f'Đã tồn tại bản ghi chấm công cho nhân viên {record.employee.full_name} vào ngày {record.date}')
				return redirect('attendance_sheet_detail', pk=record.sheet.pk)

			record.save()
			messages.success(request, 'Bản ghi chấm công đã được tạo thành công.')
			return redirect('attendance_sheet_detail', pk=record.sheet.pk)
	else:
		initial_data = {}
		if attendance_sheet:
			# Thiết lập ngày mặc định là ngày hiện tại
			initial_data['date'] = timezone.now().date()

		form = AttendanceRecordForm(initial=initial_data)

	# Lấy danh sách bảng chấm công và nhân viên để hiển thị trong form
	attendance_sheets = AttendanceSheet.objects.filter(is_locked=False).order_by('-year', '-month')

	employees_queryset = Employee.objects.filter(is_active=True)
	if attendance_sheet:
		# Nếu có bảng chấm công, chỉ hiển thị nhân viên thuộc vị trí áp dụng
		positions = attendance_sheet.positions.all()
		employees_queryset = employees_queryset.filter(position__in=positions)

	context = {
		'form': form,
		'attendance_sheet': attendance_sheet,
		'employee': employee,
		'attendance_sheets': attendance_sheets,
		'employees': employees_queryset,
		'title': 'Thêm dữ liệu chấm công',
	}
	return render(request, 'attendance/attendance_record_form.html', context)


@login_required
def attendance_record_update(request, pk):
	record = get_object_or_404(AttendanceRecord, pk=pk)

	if record.sheet.is_locked:
		messages.error(request, 'Bảng chấm công đã bị khóa, không thể chỉnh sửa.')
		return redirect('attendance_sheet_detail', pk=record.sheet.pk)

	if request.method == 'POST':
		form = AttendanceRecordForm(request.POST, instance=record)
		if form.is_valid():
			form.save()
			messages.success(request, 'Bản ghi chấm công đã được cập nhật thành công.')
			return redirect('attendance_sheet_detail', pk=record.sheet.pk)
	else:
		form = AttendanceRecordForm(instance=record)

	context = {
		'form': form,
		'record': record,
		'attendance_sheet': record.sheet,
		'employee': record.employee,
		'title': 'Cập nhật dữ liệu chấm công',
	}
	return render(request, 'attendance/attendance_record_form.html', context)


@login_required
def attendance_record_delete(request, pk):
	record = get_object_or_404(AttendanceRecord, pk=pk)
	sheet_id = record.sheet.pk

	if record.sheet.is_locked:
		messages.error(request, 'Bảng chấm công đã bị khóa, không thể xóa dữ liệu.')
		return redirect('attendance_sheet_detail', pk=sheet_id)

	if request.method == 'POST':
		record.delete()
		messages.success(request, 'Bản ghi chấm công đã được xóa thành công.')
		return redirect('attendance_sheet_detail', pk=sheet_id)

	context = {
		'record': record,
		'title': 'Xác nhận xóa bản ghi chấm công',
	}
	return render(request, 'attendance/attendance_record_confirm_delete.html', context)


@login_required
def work_shift_list(request):
	work_shifts = WorkShift.objects.all().order_by('start_time')

	context = {
		'work_shifts': work_shifts,
	}
	return render(request, 'attendance/work_shift_list.html', context)


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

	context = {
		'form': form,
		'title': 'Thêm ca làm việc',
	}
	return render(request, 'attendance/work_shift_form.html', context)


@login_required
def work_shift_update(request, pk):
	work_shift = get_object_or_404(WorkShift, pk=pk)

	if request.method == 'POST':
		form = WorkShiftForm(request.POST, instance=work_shift)
		if form.is_valid():
			form.save()
			messages.success(request, 'Ca làm việc đã được cập nhật thành công.')
			return redirect('work_shift_list')
	else:
		form = WorkShiftForm(instance=work_shift)

	context = {
		'form': form,
		'work_shift': work_shift,
		'title': 'Cập nhật ca làm việc',
	}
	return render(request, 'attendance/work_shift_form.html', context)


@login_required
def transfer_attendance_data(request, sheet_id):
	attendance_sheet = get_object_or_404(AttendanceSheet, pk=sheet_id)

	if attendance_sheet.is_transferred:
		messages.warning(request, 'Bảng chấm công này đã được chuyển tính lương trước đó.')
		return redirect('attendance_sheet_detail', pk=sheet_id)

	if request.method == 'POST':
		# Thực hiện chuyển dữ liệu tính lương
		# Đây là nơi bạn sẽ thêm logic để chuyển dữ liệu từ bảng chấm công sang bảng lương

		# Cập nhật trạng thái đã chuyển
		attendance_sheet.is_transferred = True
		attendance_sheet.is_locked = True  # Khóa bảng chấm công sau khi chuyển
		attendance_sheet.save()

		messages.success(request, 'Dữ liệu chấm công đã được chuyển sang tính lương thành công.')
		return redirect('attendance_sheet_detail', pk=sheet_id)

	# Lấy thông tin tổng hợp từ bảng chấm công
	attendance_records = AttendanceRecord.objects.filter(sheet=attendance_sheet)
	total_records = attendance_records.count()

	context = {
		'attendance_sheet': attendance_sheet,
		'total_records': total_records,
		'title': 'Chuyển dữ liệu tính lương',
	}
	return render(request, 'attendance/transfer_attendance_data.html', context)


@login_required
def export_attendance_sheet(request, pk):
	attendance_sheet = get_object_or_404(AttendanceSheet, pk=pk)
	attendance_records = AttendanceRecord.objects.filter(sheet=attendance_sheet).select_related('employee',
																								'work_shift')

	response = HttpResponse(content_type='text/csv')
	response[
		'Content-Disposition'] = f'attachment; filename="bang_cham_cong_{attendance_sheet.month}_{attendance_sheet.year}.csv"'

	writer = csv.writer(response)
	writer.writerow(
		['Mã NV', 'Họ và tên', 'Vị trí', 'Ngày', 'Trạng thái', 'Giờ vào', 'Giờ ra', 'Số giờ làm việc', 'Ca làm việc',
		 'Ghi chú'])

	for record in attendance_records:
		writer.writerow([
			record.employee.code,
			record.employee.full_name,
			record.employee.position.name if record.employee.position else '',
			record.date.strftime('%d/%m/%Y'),
			record.get_status_display(),
			record.check_in.strftime('%H:%M') if record.check_in else '',
			record.check_out.strftime('%H:%M') if record.check_out else '',
			record.working_hours,
			record.work_shift.name if record.work_shift else '',
			record.note or ''
		])

	return response


def payroll_dashboard(request):
	# Logic xử lý cho dashboard của bảng lương
	return render(request, 'payroll/dashboard.html')


def payroll_template_list(request):
	templates = PayrollTemplate.objects.all().order_by('-created_at')
	return render(request, 'payroll/payroll_template_list.html', {'templates': templates})


def payroll_template_create(request):
	if request.method == 'POST':
		form = PayrollTemplateForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('payroll_template_list')
	else:
		form = PayrollTemplateForm()

	return render(request, 'payroll/payroll_template_form.html', {'form': form})


def payroll_template_detail(request, pk):
	template = get_object_or_404(PayrollTemplate, pk=pk)
	components = template.components.all()

	return render(request, 'payroll/payroll_template_detail.html', {
		'template': template,
		'components': components
	})


def payroll_component_create(request, template_id):
	template = get_object_or_404(PayrollTemplate, pk=template_id)

	if request.method == 'POST':
		form = PayrollComponentForm(request.POST)
		if form.is_valid():
			component = form.save(commit=False)
			component.payroll_template = template
			component.save()
			return redirect('payroll_template_detail', pk=template_id)
	else:
		form = PayrollComponentForm()

	return render(request, 'payroll/payroll_component_form.html', {
		'form': form,
		'template': template
	})


def payroll_list(request):
	templates = PayrollTemplate.objects.filter(is_active=True)
	return render(request, 'payroll/payroll_list.html', {'templates': templates})


def payroll_create(request):
	if request.method == 'POST':
		form = PayrollTemplateForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('payroll_list')
	else:
		form = PayrollTemplateForm()

	return render(request, 'payroll/payroll_form.html', {'form': form})


def payroll_detail(request, pk):
	template = get_object_or_404(PayrollTemplate, pk=pk)
	return render(request, 'payroll/payroll_detail.html', {'template': template})

def home(request):
    return render(request, 'home.html')

def payroll_dashboard(request):
    return render(request, 'payroll/dashboard.html')