from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone

from .models import Employee, Department, Position, Contract, WorkHistory, SalaryHistory
from .forms import (EmployeeForm, ContractForm, WorkHistoryForm, SalaryHistoryForm,
                    ContractFilterForm)


# Employee views
@login_required
def employee_list(request):
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

    positions = Position.objects.filter(is_active=True)
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
    work_history = WorkHistory.objects.filter(employee=employee).order_by('-start_date')
    salary_history = SalaryHistory.objects.filter(employee=employee).order_by('-effective_date')

    context = {
        'employee': employee,
        'contracts': contracts,
        'work_history': work_history,
        'salary_history': salary_history,
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


# Contract views
@login_required
def contract_list(request):
    form = ContractFilterForm(request.GET)
    # Chỉ select_related các trường tồn tại
    contracts = Contract.objects.all().select_related('employee', 'position', 'department')

    if form.is_valid():
        search = form.cleaned_data.get('search')
        contract_type = form.cleaned_data.get('contract_type')
        department = form.cleaned_data.get('department')
        date_from = form.cleaned_data.get('date_from')
        date_to = form.cleaned_data.get('date_to')
        status = form.cleaned_data.get('status')

        if search:
            contracts = contracts.filter(
                Q(contract_number__icontains=search) |
                Q(employee__full_name__icontains=search) |
                Q(employee__code__icontains=search)
            )

        if contract_type:
            contracts = contracts.filter(contract_type=contract_type)

        if department:
            # Lọc theo department của contract hoặc position
            contracts = contracts.filter(
                Q(department=department) |
                Q(position__department=department)
            )

        if date_from:
            contracts = contracts.filter(start_date__gte=date_from)

        if date_to:
            contracts = contracts.filter(start_date__lte=date_to)

        if status:
            if status == 'active':
                contracts = contracts.filter(is_active=True)
            elif status == 'inactive':
                contracts = contracts.filter(is_active=False)

    # Phân trang
    paginator = Paginator(contracts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Thống kê
    total_contracts = contracts.count()
    active_contracts = contracts.filter(is_active=True).count()
    expiring_contracts = contracts.filter(
        is_active=True,
        end_date__isnull=False,
        end_date__lte=timezone.now().date() + timezone.timedelta(days=30)
    ).count()

    context = {
        'page_obj': page_obj,
        'filter_form': form,
        'total_contracts': total_contracts,
        'active_contracts': active_contracts,
        'expiring_contracts': expiring_contracts,
    }
    return render(request, 'employees/contract_list.html', context)

@login_required
def contract_create(request, employee_id=None):
    employee = None
    if employee_id:
        employee = get_object_or_404(Employee, pk=employee_id)

    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            contract = form.save(commit=False)
            if employee:
                contract.employee = employee
            else:
                employee_id = request.POST.get('employee_id')
                if not employee_id:
                    messages.error(request, 'Vui lòng chọn nhân viên')
                    return redirect('contract_create_general')
                employee = get_object_or_404(Employee, pk=employee_id)
                contract.employee = employee

            # Nếu không có ngày ký, sử dụng ngày hiện tại
            if not contract.sign_date:
                contract.sign_date = timezone.now().date()

            # Nếu không có tên hợp đồng, tạo tên mặc định
            if not contract.contract_name:
                contract.contract_name = f"Hợp đồng {contract.get_contract_type_display()} - {employee.full_name}"

            # Nếu không có đơn vị, sử dụng đơn vị của vị trí
            if not contract.department and contract.position and contract.position.department:
                contract.department = contract.position.department

            contract.save()
            messages.success(request, f'Hợp đồng mới cho nhân viên {employee.full_name} đã được tạo thành công')

            if 'save_and_new' in request.POST:
                return redirect('contract_create_general')
            return redirect('contract_detail', pk=contract.pk)
    else:
        # Tạo số hợp đồng tự động
        last_contract = Contract.objects.order_by('-contract_number').first()
        next_number = 'HD0000001'
        if last_contract and last_contract.contract_number.startswith('HD'):
            try:
                num = int(last_contract.contract_number[2:])
                next_number = f'HD{(num + 1):07d}'
            except ValueError:
                pass

        initial_data = {
            'contract_number': next_number,
            'sign_date': timezone.now().date(),
            'start_date': timezone.now().date(),
        }

        if employee:
            initial_data['position'] = employee.position
            if employee.position and employee.position.department:
                initial_data['department'] = employee.position.department

        form = ContractForm(initial=initial_data)

    context = {
        'form': form,
        'employee': employee,
    }
    return render(request, 'employees/contract_form.html', context)


@login_required
def contract_detail(request, pk):
    contract = get_object_or_404(Contract, pk=pk)
    context = {
        'contract': contract,
    }
    return render(request, 'employees/contract_detail.html', context)


@login_required
def contract_update(request, pk):
    contract = get_object_or_404(Contract, pk=pk)

    if request.method == 'POST':
        form = ContractForm(request.POST, instance=contract)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hợp đồng đã được cập nhật thành công')
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

    if request.method == 'POST':
        contract.is_active = False
        contract.end_date = timezone.now().date()
        contract.save()
        messages.success(request, 'Hợp đồng đã được chấm dứt')
        return redirect('contract_detail', pk=contract.pk)

    context = {
        'contract': contract,
    }
    return render(request, 'employees/contract_terminate.html', context)


# Personnel views
@login_required
def personnel_overview(request):
    total_employees = Employee.objects.filter(is_active=True).count()
    total_departments = Department.objects.filter(is_active=True).count()
    total_positions = Position.objects.filter(is_active=True).count()

    context = {
        'total_employees': total_employees,
        'total_departments': total_departments,
        'total_positions': total_positions,
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

    positions = Position.objects.filter(is_active=True)

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

@login_required
def contract_create_general(request):
    return contract_create(request)