from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Employee, Department, Position, Contract, WorkHistory, SalaryHistory
from .forms import EmployeeForm, ContractForm, WorkHistoryForm, SalaryHistoryForm


# Employee views
@login_required
def employee_list(request):
    search_query = request.GET.get('search', '')
    position_filter = request.GET.get('position', '')
    department_filter = request.GET.get('department', '')

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

    if department_filter:
        employees = employees.filter(department_id=department_filter)

    positions = Position.objects.filter(is_active=True)
    departments = Department.objects.filter(is_active=True)

    paginator = Paginator(employees, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'positions': positions,
        'departments': departments,
        'search_query': search_query,
        'position_filter': position_filter,
        'department_filter': department_filter,
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
            employee = form.save()
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
            employee = form.save()
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
def contract_create(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)  # Lấy nhân viên theo ID
    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            contract = form.save(commit=False)  # Tạo đối tượng hợp đồng nhưng chưa lưu vào DB
            contract.employee = employee  # Gắn hợp đồng với nhân viên đã chọn
            contract.save()  # Lưu hợp đồng
            messages.success(request, f'Hợp đồng mới cho nhân viên {employee.full_name} đã được tạo thành công')
            return redirect('employee_detail', pk=employee.pk)  # Chuyển hướng đến chi tiết nhân viên
    else:
        form = ContractForm()  # Hiển thị form khi người dùng truy cập lần đầu

    context = {
        'form': form,
        'employee': employee,
        'title': 'Tạo hợp đồng mới',
    }
    return render(request, 'employees/contract_form.html', context)


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
    department_filter = request.GET.get('department', '')

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

    if department_filter:
        employees = employees.filter(department_id=department_filter)

    positions = Position.objects.filter(is_active=True)
    departments = Department.objects.filter(is_active=True)

    paginator = Paginator(employees, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'positions': positions,
        'departments': departments,
        'search_query': search_query,
        'position_filter': position_filter,
        'department_filter': department_filter,
    }
    return render(request, 'personnel/profile_list.html', context)
