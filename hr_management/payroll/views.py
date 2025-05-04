from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PayrollTemplate, PayrollComponent, Payroll, PayrollDetail
from employees.models import Employee, Position
from attendance.models import AttendanceSheet
from .forms import PayrollTemplateForm, PayrollComponentForm, PayrollForm
from .models import PayrollTemplate, PayrollComponent, Payroll, PayrollDetail

@login_required
def payroll_dashboard(request):
	payrolls = Payroll.objects.all().order_by('-created_at')[:5]
	return render(request, 'payroll/dashboard.html', {'payrolls': payrolls})


@login_required
def payroll_template_list(request):
	templates = PayrollTemplate.objects.all().order_by('-created_at')
	position_filter = request.GET.get('position')

	if position_filter:
		templates = templates.filter(positions__id=position_filter)

	positions = Position.objects.all()

	return render(request, 'payroll/template_list.html', {
		'templates': templates,
		'positions': positions,
		'position_filter': position_filter
	})


@login_required
def payroll_template_create(request):
	if request.method == 'POST':
		form = PayrollTemplateForm(request.POST)
		if form.is_valid():
			template = form.save()
			messages.success(request, 'Mẫu bảng lương đã được tạo thành công.')
			return redirect('payroll_template_detail', pk=template.pk)
	else:
		form = PayrollTemplateForm()

	return render(request, 'payroll/template_form.html', {'form': form})


@login_required
def payroll_template_detail(request, pk):
	template = get_object_or_404(PayrollTemplate, pk=pk)
	components = PayrollComponent.objects.filter(template=template)

	return render(request, 'payroll/template_detail.html', {
		'template': template,
		'components': components
	})


@login_required
def payroll_component_create(request, template_id):
	template = get_object_or_404(PayrollTemplate, pk=template_id)

	if request.method == 'POST':
		form = PayrollComponentForm(request.POST)
		if form.is_valid():
			component = form.save(commit=False)
			component.template = template
			component.save()
			messages.success(request, 'Thành phần lương đã được tạo thành công.')
			return redirect('payroll_template_detail', pk=template_id)
	else:
		form = PayrollComponentForm()

	return render(request, 'payroll/component_form.html', {
		'form': form,
		'template': template
	})


@login_required
def payroll_list(request):
	payrolls = Payroll.objects.all().order_by('-year', '-month')
	position_filter = request.GET.get('position')

	if position_filter:
		payrolls = payrolls.filter(positions__id=position_filter)

	positions = Position.objects.all()

	return render(request, 'payroll/payroll_list.html', {
		'payrolls': payrolls,
		'positions': positions,
		'position_filter': position_filter
	})


@login_required
def payroll_create(request):
	if request.method == 'POST':
		form = PayrollForm(request.POST)
		if form.is_valid():
			payroll = form.save()

			# Tạo chi tiết bảng lương cho từng nhân viên
			positions = payroll.positions.all()
			employees = Employee.objects.filter(position__in=positions, is_active=True)

			for employee in employees:
				# Lấy lương cơ bản từ hợp đồng mới nhất
				contract = employee.contracts.filter(is_active=True).first()
				base_salary = contract.basic_salary if contract else 0

				# Tính số ngày công từ bảng chấm công
				actual_workdays = 0
				if payroll.attendance_sheet:
					from django.db.models import Sum
					records = payroll.attendance_sheet.records.filter(
						employee=employee,
						status='present'
					)
					actual_workdays = records.count()

				# Tạo chi tiết bảng lương
				PayrollDetail.objects.create(
					payroll=payroll,
					employee=employee,
					base_salary=base_salary,
					actual_workdays=actual_workdays,
					total_income=base_salary,  # Đơn giản hóa, chỉ tính lương cơ bản
					net_salary=base_salary  # Đơn giản hóa, chưa tính khấu trừ
				)

			messages.success(request, 'Bảng lương đã được tạo thành công.')
			return redirect('payroll_detail', pk=payroll.pk)
	else:
		form = PayrollForm()

	return render(request, 'payroll/payroll_form.html', {'form': form})


@login_required
def payroll_detail(request, pk):
	payroll = get_object_or_404(Payroll, pk=pk)
	details = PayrollDetail.objects.filter(payroll=payroll)

	return render(request, 'payroll/payroll_detail.html', {
		'payroll': payroll,
		'details': details
	})
