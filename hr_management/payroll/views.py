from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
import csv
import datetime
from .forms import PayrollPeriodForm

from .models import (
	PayrollTemplate, PayrollTemplateItem, PayrollPeriod,
	PayrollData, PayrollDataDetail, Payroll, PayrollDetail,
	PayrollPayment, PayrollPaymentDetail, Payslip
)
from .forms import (
	PayrollTemplateForm, PayrollTemplateItemForm,
	PayrollDataForm, PayrollDataDetailForm, PayrollForm, PayrollDetailForm,
	PayrollPaymentForm, PayrollPaymentDetailForm, PayslipForm,
	PayrollFilterForm, PayrollDataFilterForm, PayrollPaymentFilterForm
)

def payroll_template_detail(request, pk):
	# Lấy đối tượng PayrollTemplate theo pk
	payroll_template = get_object_or_404(PayrollTemplate, pk=pk)

	# Trả về chi tiết mẫu bảng lương
	return render(request, 'payroll_template_detail.html', {'payroll_template': payroll_template})

# Payroll Template Views
@login_required
def payroll_template_list(request):
	search_query = request.GET.get('search', '')
	templates = PayrollTemplate.objects.all()

	if search_query:
		templates = templates.filter(
			Q(code__icontains=search_query) |
			Q(name__icontains=search_query)
		)

	paginator = Paginator(templates, 10)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	context = {
		'page_obj': page_obj,
		'search_query': search_query,
	}
	return render(request, 'payroll/template_list.html', context)


@login_required
def payroll_template_detail(request, pk):
	template = get_object_or_404(PayrollTemplate, pk=pk)
	items = template.items.all().order_by('order')

	context = {
		'template': template,
		'items': items,
	}
	return render(request, 'payroll/template_detail.html', context)


@login_required
def payroll_template_create(request):
	if request.method == 'POST':
		form = PayrollTemplateForm(request.POST)
		if form.is_valid():
			template = form.save()
			messages.success(request, f'Mẫu bảng lương {template.name} đã được tạo thành công')
			return redirect('payroll_template_detail', pk=template.pk)
	else:
		form = PayrollTemplateForm()

	context = {
		'form': form,
		'title': 'Thêm mẫu bảng lương mới',
	}
	return render(request, 'payroll/template_form.html', context)


@login_required
def payroll_template_update(request, pk):
	template = get_object_or_404(PayrollTemplate, pk=pk)
	if request.method == 'POST':
		form = PayrollTemplateForm(request.POST, instance=template)
		if form.is_valid():
			template = form.save()
			messages.success(request, f'Mẫu bảng lương {template.name} đã được cập nhật')
			return redirect('payroll_template_detail', pk=template.pk)
	else:
		form = PayrollTemplateForm(instance=template)

	context = {
		'form': form,
		'template': template,
		'title': 'Cập nhật mẫu bảng lương',
	}
	return render(request, 'payroll/template_form.html', context)


@login_required
def payroll_template_item_create(request, template_id):
	template = get_object_or_404(PayrollTemplate, pk=template_id)
	if request.method == 'POST':
		form = PayrollTemplateItemForm(request.POST)
		if form.is_valid():
			item = form.save(commit=False)
			item.template = template
			item.save()
			messages.success(request, f'Mục {item.name} đã được thêm vào mẫu bảng lương')
			return redirect('payroll_template_detail', pk=template.pk)
	else:
		form = PayrollTemplateItemForm()

	context = {
		'form': form,
		'template': template,
		'title': 'Thêm mục vào mẫu bảng lương',
	}
	return render(request, 'payroll/template_item_form.html', context)


@login_required
def payroll_template_item_update(request, pk):
	item = get_object_or_404(PayrollTemplateItem, pk=pk)
	if request.method == 'POST':
		form = PayrollTemplateItemForm(request.POST, instance=item)
		if form.is_valid():
			item = form.save()
			messages.success(request, f'Mục {item.name} đã được cập nhật')
			return redirect('payroll_template_detail', pk=item.template.pk)
	else:
		form = PayrollTemplateItemForm(instance=item)

	context = {
		'form': form,
		'item': item,
		'template': item.template,
		'title': 'Cập nhật mục bảng lương',
	}
	return render(request, 'payroll/template_item_form.html', context)


# Payroll Period Views
@login_required
def payroll_period_list(request):
	search_query = request.GET.get('search', '')
	periods = PayrollPeriod.objects.all().order_by('-start_date')

	if search_query:
		periods = periods.filter(
			Q(code__icontains=search_query) |
			Q(name__icontains=search_query)
		)

	paginator = Paginator(periods, 10)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	context = {
		'page_obj': page_obj,
		'search_query': search_query,
	}
	return render(request, 'payroll/period_list.html', context)


@login_required
def payroll_period_detail(request, pk):
	period = get_object_or_404(PayrollPeriod, pk=pk)
	payroll_data = period.payroll_data.all()
	payrolls = period.payrolls.all()

	context = {
		'period': period,
		'payroll_data': payroll_data,
		'payrolls': payrolls,
	}
	return render(request, 'payroll/period_detail.html', context)


@login_required
def payroll_period_create(request):
	if request.method == 'POST':
		form = PayrollPeriodForm(request.POST)
		if form.is_valid():
			period = form.save()
			messages.success(request, f'Kỳ lương {period.name} đã được tạo thành công')
			return redirect('payroll_period_detail', pk=period.pk)
	else:
		form = PayrollPeriodForm()

	context = {
		'form': form,
		'title': 'Thêm kỳ lương mới',
	}
	return render(request, 'payroll/period_form.html', context)


@login_required
def payroll_period_update(request, pk):
	period = get_object_or_404(PayrollPeriod, pk=pk)
	if request.method == 'POST':
		form = PayrollPeriodForm(request.POST, instance=period)
		if form.is_valid():
			period = form.save()
			messages.success(request, f'Kỳ lương {period.name} đã được cập nhật')
			return redirect('payroll_period_detail', pk=period.pk)
	else:
		form = PayrollPeriodForm(instance=period)

	context = {
		'form': form,
		'period': period,
		'title': 'Cập nhật kỳ lương',
	}
	return render(request, 'payroll/period_form.html', context)


# Payroll Data Views
@login_required
def payroll_data_list(request):
	form = PayrollDataFilterForm(request.GET)
	payroll_data = PayrollData.objects.all().order_by('-period__start_date')

	if form.is_valid():
		period = form.cleaned_data.get('period')
		department = form.cleaned_data.get('department')
		status = form.cleaned_data.get('status')
		search = form.cleaned_data.get('search')

		if period:
			payroll_data = payroll_data.filter(period=period)

		if department:
			payroll_data = payroll_data.filter(department=department)

		if status:
			payroll_data = payroll_data.filter(status=status)

		if search:
			payroll_data = payroll_data.filter(
				Q(period__name__icontains=search) |
				Q(department__name__icontains=search)
			)

	paginator = Paginator(payroll_data, 10)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	context = {
		'page_obj': page_obj,
		'form': form,
	}
	return render(request, 'payroll/data_list.html', context)


@login_required
def payroll_data_detail(request, pk):
	payroll_data = get_object_or_404(PayrollData, pk=pk)
	details = payroll_data.details.all()

	context = {
		'payroll_data': payroll_data,
		'details': details,
	}
	return render(request, 'payroll/data_detail.html', context)


@login_required
def payroll_data_create(request):
	if request.method == 'POST':
		form = PayrollDataForm(request.POST)
		if form.is_valid():
			payroll_data = form.save(commit=False)
			payroll_data.status = 'draft'
			payroll_data.save()
			messages.success(request, f'Dữ liệu tính lương cho {payroll_data.department.name} đã được tạo thành công')
			return redirect('payroll_data_detail', pk=payroll_data.pk)
	else:
		form = PayrollDataForm()

	context = {
		'form': form,
		'title': 'Thêm dữ liệu tính lương mới',
	}
	return render(request, 'payroll/data_form.html', context)


@login_required
def payroll_data_update(request, pk):
	payroll_data = get_object_or_404(PayrollData, pk=pk)
	if request.method == 'POST':
		form = PayrollDataForm(request.POST, instance=payroll_data)
		if form.is_valid():
			payroll_data = form.save()
			messages.success(request, f'Dữ liệu tính lương cho {payroll_data.department.name} đã được cập nhật')
			return redirect('payroll_data_detail', pk=payroll_data.pk)
	else:
		form = PayrollDataForm(instance=payroll_data)

	context = {
		'form': form,
		'payroll_data': payroll_data,
		'title': 'Cập nhật dữ liệu tính lương',
	}
	return render(request, 'payroll/data_form.html', context)


@login_required
def payroll_data_submit(request, pk):
	payroll_data = get_object_or_404(PayrollData, pk=pk)
	if payroll_data.status == 'draft':
		payroll_data.submit(request.user.username)
		messages.success(request, f'Dữ liệu tính lương cho {payroll_data.department.name} đã được nộp')
	return redirect('payroll_data_detail', pk=payroll_data.pk)


@login_required
def payroll_data_approve(request, pk):
	payroll_data = get_object_or_404(PayrollData, pk=pk)
	if payroll_data.status == 'submitted':
		payroll_data.approve(request.user.username)
		messages.success(request, f'Dữ liệu tính lương cho {payroll_data.department.name} đã được duyệt')
	return redirect('payroll_data_detail', pk=payroll_data.pk)


@login_required
def payroll_data_reject(request, pk):
	payroll_data = get_object_or_404(PayrollData, pk=pk)
	if payroll_data.status == 'submitted':
		payroll_data.reject()
		messages.success(request, f'Dữ liệu tính lương cho {payroll_data.department.name} đã bị từ chối')
	return redirect('payroll_data_detail', pk=payroll_data.pk)


@login_required
def payroll_data_detail_create(request, payroll_data_id):
	payroll_data = get_object_or_404(PayrollData, pk=payroll_data_id)
	if request.method == 'POST':
		form = PayrollDataDetailForm(request.POST)
		if form.is_valid():
			detail = form.save(commit=False)
			detail.payroll_data = payroll_data
			detail.save()
			messages.success(request, f'Dữ liệu cho nhân viên {detail.employee.full_name} đã được thêm thành công')
			return redirect('payroll_data_detail', pk=payroll_data.pk)
	else:
		# Lấy danh sách nhân viên thuộc phòng ban
		employees = Employee.objects.filter(department=payroll_data.department, is_active=True)
		form = PayrollDataDetailForm()
		form.fields['employee'].queryset = employees

	context = {
		'form': form,
		'payroll_data': payroll_data,
		'title': 'Thêm dữ liệu nhân viên',
	}
	return render(request, 'payroll/data_detail_form.html', context)


@login_required
def payroll_data_detail_update(request, pk):
	detail = get_object_or_404(PayrollDataDetail, pk=pk)
	if request.method == 'POST':
		form = PayrollDataDetailForm(request.POST, instance=detail)
		if form.is_valid():
			detail = form.save()
			messages.success(request, f'Dữ liệu cho nhân viên {detail.employee.full_name} đã được cập nhật')
			return redirect('payroll_data_detail', pk=detail.payroll_data.pk)
	else:
		form = PayrollDataDetailForm(instance=detail)

	context = {
		'form': form,
		'detail': detail,
		'payroll_data': detail.payroll_data,
		'title': 'Cập nhật dữ liệu nhân viên',
	}
	return render(request, 'payroll/data_detail_form.html', context)


# Payroll Views
@login_required
def payroll_list(request):
	form = PayrollFilterForm(request.GET)
	payrolls = Payroll.objects.all().order_by('-period__start_date')

	if form.is_valid():
		period = form.cleaned_data.get('period')
		department = form.cleaned_data.get('department')
		status = form.cleaned_data.get('status')
		search = form.cleaned_data.get('search')

		if period:
			payrolls = payrolls.filter(period=period)

		if status:
			payrolls = payrolls.filter(status=status)

		if search:
			payrolls = payrolls.filter(
				Q(code__icontains=search) |
				Q(name__icontains=search)
			)

		if department:
			# Lọc theo phòng ban (cần join với PayrollDetail và Employee)
			payrolls = payrolls.filter(details__employee__department=department).distinct()

	paginator = Paginator(payrolls, 10)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	context = {
		'page_obj': page_obj,
		'form': form,
	}
	return render(request, 'payroll/payroll_list.html', context)


@login_required
def payroll_detail(request, pk):
	payroll = get_object_or_404(Payroll, pk=pk)
	details = payroll.details.all()
	payments = payroll.payments.all()

	# Tính tổng
	total_gross = details.aggregate(total=Sum('gross_salary'))['total'] or 0
	total_net = details.aggregate(total=Sum('net_salary'))['total'] or 0
	total_paid = payments.aggregate(total=Sum('paid_amount'))['total'] or 0

	context = {
		'payroll': payroll,
		'details': details,
		'payments': payments,
		'total_gross': total_gross,
		'total_net': total_net,
		'total_paid': total_paid,
	}
	return render(request, 'payroll/payroll_detail.html', context)


@login_required
def payroll_create(request):
	if request.method == 'POST':
		form = PayrollForm(request.POST)
		if form.is_valid():
			payroll = form.save(commit=False)
			payroll.status = 'draft'
			payroll.created_by = request.user.username
			payroll.save()
			messages.success(request, f'Bảng lương {payroll.name} đã được tạo thành công')
			return redirect('payroll_detail', pk=payroll.pk)
	else:
		form = PayrollForm()

	context = {
		'form': form,
		'title': 'Tạo bảng lương mới',
	}
	return render(request, 'payroll/payroll_form.html', context)


@login_required
def payroll_update(request, pk):
	payroll = get_object_or_404(Payroll, pk=pk)
	if request.method == 'POST':
		form = PayrollForm(request.POST, instance=payroll)
		if form.is_valid():
			payroll = form.save()
			messages.success(request, f'Bảng lương {payroll.name} đã được cập nhật')
			return redirect('payroll_detail', pk=payroll.pk)
	else:
		form = PayrollForm(instance=payroll)

	context = {
		'form': form,
		'payroll': payroll,
		'title': 'Cập nhật bảng lương',
	}
	return render(request, 'payroll/payroll_form.html', context)


@login_required
def payroll_approve(request, pk):
	payroll = get_object_or_404(Payroll, pk=pk)
	if payroll.status in ['draft', 'processing']:
		payroll.approve(request.user.username)
		messages.success(request, f'Bảng lương {payroll.name} đã được duyệt')
	return redirect('payroll_detail', pk=payroll.pk)


@login_required
def payroll_detail_create(request, payroll_id):
	payroll = get_object_or_404(Payroll, pk=payroll_id)
	if request.method == 'POST':
		form = PayrollDetailForm(request.POST)
		if form.is_valid():
			detail = form.save(commit=False)
			detail.payroll = payroll
			detail.save()
			messages.success(request,
			                 f'Dữ liệu lương cho nhân viên {detail.employee.full_name} đã được thêm thành công')
			return redirect('payroll_detail', pk=payroll.pk)
	else:
		form = PayrollDetailForm()

	context = {
		'form': form,
		'payroll': payroll,
		'title': 'Thêm dữ liệu lương nhân viên',
	}
	return render(request, 'payroll/payroll_detail_form.html', context)


@login_required
def payroll_detail_update(request, pk):
	detail = get_object_or_404(PayrollDetail, pk=pk)
	if request.method == 'POST':
		form = PayrollDetailForm(request.POST, instance=detail)
		if form.is_valid():
			detail = form.save()
			messages.success(request, f'Dữ liệu lương cho nhân viên {detail.employee.full_name} đã được cập nhật')
			return redirect('payroll_detail', pk=detail.payroll.pk)
	else:
		form = PayrollDetailForm(instance=detail)

	context = {
		'form': form,
		'detail': detail,
		'payroll': detail.payroll,
		'title': 'Cập nhật dữ liệu lương nhân viên',
	}
	return render(request, 'payroll/payroll_detail_form.html', context)


@login_required
def payroll_calculate(request, pk):
	payroll = get_object_or_404(Payroll, pk=pk)

	# Lấy dữ liệu từ PayrollData đã được duyệt
	approved_data = PayrollData.objects.filter(period=payroll.period, status='approved')

	# Xóa dữ liệu cũ nếu có
	PayrollDetail.objects.filter(payroll=payroll).delete()

	# Tạo dữ liệu mới từ PayrollDataDetail
	for data in approved_data:
		for detail in data.details.all():
			# Tính toán các giá trị
			gross_salary = detail.basic_salary + detail.allowance + detail.bonus

			# Tính thuế TNCN (giả định)
			taxable_income = gross_salary - insurance - 11000000  # Giảm trừ gia cảnh
			if taxable_income <= 0:
				tax = 0
			elif taxable_income <= 5000000:
				tax = taxable_income * 0.05
			elif taxable_income <= 10000000:
				tax = 250000 + (taxable_income - 5000000) * 0.1
			elif taxable_income <= 18000000:
				tax = 750000 + (taxable_income - 10000000) * 0.15
			elif taxable_income <= 32000000:
				tax = 1950000 + (taxable_income - 18000000) * 0.2
			elif taxable_income <= 52000000:
				tax = 4750000 + (taxable_income - 32000000) * 0.25
			elif taxable_income <= 80000000:
				tax = 9750000 + (taxable_income - 52000000) * 0.3
			else:
				tax = 18150000 + (taxable_income - 80000000) * 0.35

			net_salary = gross_salary - tax - detail.deduction

			# Tạo PayrollDetail mới
			PayrollDetail.objects.create(
				payroll=payroll,
				employee=detail.employee,
				working_days=detail.working_days,
				overtime_hours=detail.overtime_hours,
				leave_days=detail.leave_days,
				basic_salary=detail.basic_salary,
				allowance=detail.allowance,
				bonus=detail.bonus,
				deduction=detail.deduction,
				gross_salary=gross_salary,
				tax=tax,
				net_salary=net_salary
			)

	# Cập nhật trạng thái bảng lương
	payroll.status = 'processing'
	payroll.save()

	messages.success(request, f'Đã tính toán lương cho {payroll.name}')
	return redirect('payroll_detail', pk=payroll.pk)


@login_required
def payroll_export_csv(request, pk):
	payroll = get_object_or_404(Payroll, pk=pk)
	details = payroll.details.all()

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = f'attachment; filename="{payroll.code}_{payroll.name}.csv"'

	writer = csv.writer(response)
	writer.writerow([
		'Mã NV', 'Họ và tên', 'Phòng ban', 'Vị trí',
		'Ngày công', 'Giờ làm thêm', 'Ngày nghỉ',
		'Lương cơ bản', 'Phụ cấp', 'Thưởng', 'Khấu trừ',
		'Tổng thu nhập', 'Bảo hiểm', 'Thuế TNCN', 'Thực lãnh'
	])

	for detail in details:
		writer.writerow([
			detail.employee.code,
			detail.employee.full_name,
			detail.employee.department.name if detail.employee.department else '',
			detail.employee.position.name if detail.employee.position else '',
			detail.working_days,
			detail.overtime_hours,
			detail.leave_days,
			detail.basic_salary,
			detail.allowance,
			detail.bonus,
			detail.deduction,
			detail.gross_salary,
			detail.tax,
			detail.net_salary
		])

	return response


# Payroll Payment Views
@login_required
def payroll_payment_list(request):
	form = PayrollPaymentFilterForm(request.GET)
	payments = PayrollPayment.objects.all().order_by('-payment_date')

	if form.is_valid():
		payroll = form.cleaned_data.get('payroll')
		status = form.cleaned_data.get('status')
		payment_method = form.cleaned_data.get('payment_method')
		search = form.cleaned_data.get('search')

		if payroll:
			payments = payments.filter(payroll=payroll)

		if status:
			payments = payments.filter(status=status)

		if payment_method:
			payments = payments.filter(payment_method=payment_method)

		if search:
			payments = payments.filter(
				Q(code__icontains=search) |
				Q(payroll__name__icontains=search)
			)

	paginator = Paginator(payments, 10)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	context = {
		'page_obj': page_obj,
		'form': form,
	}
	return render(request, 'payroll/payment_list.html', context)


@login_required
def payroll_payment_detail(request, pk):
	payment = get_object_or_404(PayrollPayment, pk=pk)
	details = payment.details.all()

	context = {
		'payment': payment,
		'details': details,
	}
	return render(request, 'payroll/payment_detail.html', context)


@login_required
@login_required
def payroll_payment_create(request, payroll_id=None):
    payroll = None
    if payroll_id:
        payroll = get_object_or_404(Payroll, pk=payroll_id)

    if request.method == 'POST':
        form = PayrollPaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.created_by = request.user.username
            payment.save()

            # Tạo chi tiết thanh toán cho từng nhân viên
            if not payroll:
                payroll = payment.payroll

            for detail in payroll.details.all():
                PayrollPaymentDetail.objects.create(
                    payment=payment,
                    employee=detail.employee,
                    amount=detail.net_salary,
                    status='pending'
                )

            messages.success(request, f'Thanh toán lương {payment.code} đã được tạo thành công')
            return redirect('payroll_payment_detail', pk=payment.pk)
    else:
        initial = {}
        if payroll:
            # Tính tổng lương thực lãnh
            total_net = payroll.details.aggregate(total=Sum('net_salary'))['total'] or 0
            initial = {
                'payroll': payroll,
                'total_amount': total_net,
                'payment_date': datetime.date.today()
            }
        form = PayrollPaymentForm(initial=initial)  # Khởi tạo form với dữ liệu ban đầu (nếu có)

    return render(request, 'payroll/payment_create.html', {'form': form})

