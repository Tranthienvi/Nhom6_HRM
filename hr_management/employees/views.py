from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Prefetch
from django.core.paginator import Paginator
from django.utils import timezone
from django.http import HttpResponse
import os
from django.conf import settings

from .models import Employee, Position, Contract
from .forms import EmployeeForm, ContractForm


# Employee views
@login_required
def employee_list(request):
	search_query = request.GET.get('search', '')
	position_filter = request.GET.get('position', '')

	# Sửa lại dòng này
	employees = Employee.objects.all()

	if search_query:
		employees = employees.filter(
			Q(code__icontains=search_query) |
			Q(full_name__icontains=search_query) |
			Q(phone__icontains=search_query) |
			Q(email__icontains=search_query)
		)

	if position_filter:
		employees = employees.filter(position_id=position_filter)

	# Nếu model Position không có trường is_active, sửa lại dòng này
	positions = Position.objects.all()  # Bỏ filter(is_active=True)
	paginator = Paginator(employees, 10)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	context = {
		'page_obj': page_obj,
		'positions': positions,
		'search_query': search_query,
		'position_filter': position_filter,
	}
	return render(request, 'employees/employee_list.html', context)


@login_required
def employee_detail(request, pk):
	employee = get_object_or_404(Employee, pk=pk)
	contracts = Contract.objects.filter(employee=employee).order_by('-start_date')

	context = {
		'employee': employee,
		'contracts': contracts,
	}
	return render(request, 'employees/employee_detail.html', context)


@login_required
def employee_create(request):
	if request.method == 'POST':
		form = EmployeeForm(request.POST, request.FILES)
		if form.is_valid():
			employee = form.save(commit=False)
			# Gộp họ tên
			employee.full_name = f"{employee.last_name} {employee.first_name}"
			employee.save()
			messages.success(request, f'Nhân viên {employee.full_name} đã được tạo thành công')
			return redirect('employee_detail', pk=employee.pk)
	else:
		form = EmployeeForm()

	context = {
		'form': form,
		'title': 'Thêm nhân viên mới',
	}
	return render(request, 'employees/employee_form.html', context)


@login_required
def employee_update(request, pk):
	employee = get_object_or_404(Employee, pk=pk)
	if request.method == 'POST':
		form = EmployeeForm(request.POST, request.FILES, instance=employee)
		if form.is_valid():
			employee = form.save(commit=False)
			# Cập nhật full_name trước khi lưu
			employee.full_name = f"{employee.last_name} {employee.first_name}"
			employee.save()
			messages.success(request, f'Thông tin nhân viên {employee.full_name} đã được cập nhật')
			return redirect('employee_detail', pk=employee.pk)
	else:
		form = EmployeeForm(instance=employee)

	context = {
		'form': form,
		'employee': employee,
		'title': 'Cập nhật thông tin nhân viên',
	}
	return render(request, 'employees/employee_form.html', context)


@login_required
def employee_deactivate(request, pk):
	employee = get_object_or_404(Employee, pk=pk)
	employee.is_active = False
	employee.save()

	messages.success(request, f'Nhân viên {employee.full_name} đã được vô hiệu hóa.')
	return redirect('employee_list')


@login_required
def employee_activate(request, pk):
	employee = get_object_or_404(Employee, pk=pk)
	employee.is_active = True
	employee.save()
	messages.success(request, f'Nhân viên {employee.full_name} đã được kích hoạt lại.')
	return redirect('employee_list')


# Contract views
@login_required
def contract_list(request):
	search_query = request.GET.get('search', '')
	status_filter = request.GET.get('status', '')
	type_filter = request.GET.get('type', '')

	contracts = Contract.objects.all().select_related('employee', 'position')

	if search_query:
		contracts = contracts.filter(
			Q(contract_number__icontains=search_query) |
			Q(employee__full_name__icontains=search_query) |
			Q(employee__code__icontains=search_query)
		)

	if status_filter:
		contracts = contracts.filter(status=status_filter)

	if type_filter:
		contracts = contracts.filter(contract_type=type_filter)

	paginator = Paginator(contracts, 10)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	context = {
		'page_obj': page_obj,
		'search_query': search_query,
		'status_filter': status_filter,
		'type_filter': type_filter,
		'contract_statuses': Contract.STATUS_CHOICES,
		'contract_types': Contract.CONTRACT_TYPE_CHOICES,
	}
	return render(request, 'employees/contract_list.html', context)


@login_required
def contract_detail(request, pk):
	contract = get_object_or_404(Contract, pk=pk)

	context = {
		'contract': contract,
	}
	return render(request, 'employees/contract_detail.html', context)


@login_required
def contract_create(request, employee_id=None):
	if request.method == 'POST':
		form = ContractForm(request.POST, request.FILES, employee_id=employee_id)
		if form.is_valid():
			contract = form.save()
			messages.success(request, f'Hợp đồng {contract.contract_number} đã được tạo thành công')

			if employee_id:
				return redirect('employee_detail', pk=employee_id)
			return redirect('contract_detail', pk=contract.pk)
	else:
		form = ContractForm(employee_id=employee_id)

	context = {
		'form': form,
		'title': 'Thêm hợp đồng mới',
		'employee_id': employee_id,
	}
	return render(request, 'employees/contract_form.html', context)


@login_required
def contract_update(request, pk):
	contract = get_object_or_404(Contract, pk=pk)
	if request.method == 'POST':
		form = ContractForm(request.POST, request.FILES, instance=contract)
		if form.is_valid():
			contract = form.save()
			messages.success(request, f'Hợp đồng {contract.contract_number} đã được cập nhật')
			return redirect('contract_detail', pk=contract.pk)
	else:
		form = ContractForm(instance=contract)

	context = {
		'form': form,
		'contract': contract,
		'title': 'Cập nhật hợp đồng',
	}
	return render(request, 'employees/contract_form.html', context)


@login_required
def contract_terminate(request, pk):
	contract = get_object_or_404(Contract, pk=pk)
	contract.status = 'terminated'
	contract.save()

	messages.success(request, f'Hợp đồng {contract.contract_number} đã được chấm dứt.')
	return redirect('contract_detail', pk=contract.pk)


@login_required
def contract_download(request, pk):
	contract = get_object_or_404(Contract, pk=pk)

	if not contract.file:
		messages.error(request, 'Không tìm thấy file hợp đồng.')
		return redirect('contract_detail', pk=contract.pk)

	file_path = os.path.join(settings.MEDIA_ROOT, contract.file.name)
	if os.path.exists(file_path):
		with open(file_path, 'rb') as fh:
			response = HttpResponse(fh.read(), content_type='application/pdf')
			response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
			return response

	messages.error(request, 'Không tìm thấy file hợp đồng.')
	return redirect('contract_detail', pk=contract.pk)


# Personnel views
@login_required
def personnel_overview(request):
	total_employees = Employee.objects.filter(is_active=True).count()
	total_positions = Position.objects.all().count()
	active_contracts = Contract.objects.filter(status='active').count()
	expiring_contracts = Contract.objects.filter(
		status='active',
		end_date__isnull=False,
		end_date__lte=timezone.now().date() + timezone.timedelta(days=30)
	).count()

	context = {
		'total_employees': total_employees,
		'total_positions': total_positions,
		'active_contracts': active_contracts,
		'expiring_contracts': expiring_contracts,
	}
	return render(request, 'personnel/overview.html', context)


@login_required
def personnel_profile(request):
	search_query = request.GET.get('search', '')
	position_filter = request.GET.get('position', '')

	employees = Employee.objects.all()

	if search_query:
		employees = employees.filter(
			Q(code__icontains=search_query) |
			Q(full_name__icontains=search_query) |
			Q(phone__icontains=search_query) |
			Q(email__icontains=search_query)
		)

	if position_filter:
		employees = employees.filter(position_id=position_filter)

	positions = Position.objects.all()

	paginator = Paginator(employees, 10)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	context = {
		'page_obj': page_obj,
		'positions': positions,
		'search_query': search_query,
		'position_filter': position_filter,
	}
	return render(request, 'personnel/profile_list.html', context)
