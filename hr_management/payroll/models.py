from django.db import models
from employees.models import Position, Department

class Employee(models.Model):
	GENDER_CHOICES = [
		('M', 'Nam'),
		('F', 'Nữ'),
		('O', 'Khác'),
	]

	STATUS_CHOICES = [
		('active', 'Đang làm việc'),
		('inactive', 'Đã nghỉ việc'),
		('on_leave', 'Đang nghỉ phép'),
		('suspended', 'Tạm đình chỉ'),
	]

	employee_id = models.CharField(max_length=20, unique=True, verbose_name="Mã nhân viên")
	first_name = models.CharField(max_length=50, verbose_name="Tên")
	last_name = models.CharField(max_length=50, verbose_name="Họ")
	date_of_birth = models.DateField(verbose_name="Ngày sinh")
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Giới tính")
	address = models.TextField(verbose_name="Địa chỉ")
	phone_number = models.CharField(max_length=15, verbose_name="Số điện thoại")
	email = models.EmailField(verbose_name="Email")
	department = models.CharField(max_length=100, verbose_name="Phòng ban")
	position = models.CharField(max_length=100, verbose_name="Chức vụ")
	hire_date = models.DateField(verbose_name="Ngày vào làm")
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="Trạng thái")

	def __str__(self):
		return f"{self.last_name} {self.first_name} ({self.employee_id})"

	class Meta:
		verbose_name = "Nhân viên"
		verbose_name_plural = "Nhân viên"


class PayrollTemplate(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=12, decimal_places=2)
    bonus = models.DecimalField(max_digits=12, decimal_places=2)
    deductions = models.DecimalField(max_digits=12, decimal_places=2)
    effective_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PayrollTemplateItem(models.Model):
	template = models.ForeignKey(PayrollTemplate, on_delete=models.CASCADE, related_name='items')
	code = models.CharField(max_length=50)
	name = models.CharField(max_length=255)

	ITEM_TYPE_CHOICES = [
		('earning', 'Thu nhập'),
		('deduction', 'Khấu trừ'),
	]
	CALCULATION_TYPE_CHOICES = [
		('fixed', 'Cố định'),
		('percentage', 'Phần trăm'),
	]

	item_type = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES)
	calculation_type = models.CharField(max_length=20, choices=CALCULATION_TYPE_CHOICES)
	order = models.PositiveIntegerField()
	is_active = models.BooleanField(default=True)
	value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Thêm trường 'value'

	def __str__(self):
		return f"{self.template.name} - {self.name}"


class PayrollPeriod(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    payment_date = models.DateField()

    STATUS_CHOICES = [
        ('draft', 'Nháp'),
        ('approved', 'Đã duyệt'),
        ('paid', 'Đã trả lương'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    # Thêm trường `template` vào model
    template = models.ForeignKey(PayrollTemplate, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class PayrollData(models.Model):
	period = models.ForeignKey(PayrollPeriod, on_delete=models.CASCADE)
	department = models.CharField(max_length=100)
	status = models.CharField(max_length=20, choices=[('pending', 'Chờ duyệt'), ('approved', 'Đã duyệt')],
	                          default='pending')
	submitted_by = models.CharField(max_length=100)
	submitted_at = models.DateTimeField(auto_now_add=True)
	approved_by = models.CharField(max_length=100, null=True, blank=True)
	approved_at = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return f"{self.department} - {self.period.name}"


class PayrollDataDetail(models.Model):
    payroll_data = models.ForeignKey(PayrollData, on_delete=models.CASCADE, related_name='details')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    working_days = models.DecimalField(max_digits=5, decimal_places=2)
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2)
    basic_salary = models.DecimalField(max_digits=12, decimal_places=2)

    # Thêm các trường còn thiếu
    leave_days = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    allowance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bonus = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deduction = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.employee.full_name} - {self.payroll_data.period.name}"



class Payroll(models.Model):
	code = models.CharField(max_length=50, unique=True)
	name = models.CharField(max_length=255)
	period = models.ForeignKey(PayrollPeriod, on_delete=models.CASCADE)
	status = models.CharField(max_length=20, choices=[('draft', 'Nháp'), ('approved', 'Đã duyệt')], default='draft')
	created_by = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True)
	approved_by = models.CharField(max_length=100, null=True, blank=True)
	approved_at = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return self.name


class PayrollDetail(models.Model):
    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    working_days = models.DecimalField(max_digits=5, decimal_places=2)
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    leave_days = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    basic_salary = models.DecimalField(max_digits=12, decimal_places=2)
    allowance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bonus = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deduction = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    insurance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    gross_salary = models.DecimalField(max_digits=12, decimal_places=2)
    net_salary = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.employee.full_name} - {self.payroll.name}"



class PayrollPayment(models.Model):
	code = models.CharField(max_length=50, unique=True)
	payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE)
	payment_date = models.DateField()
	payment_method = models.CharField(max_length=50)
	total_amount = models.DecimalField(max_digits=12, decimal_places=2)
	paid_amount = models.DecimalField(max_digits=12, decimal_places=2)

	STATUS_CHOICES = [
		('pending', 'Chờ xử lý'),
		('paid', 'Đã thanh toán'),
	]
	PAYMENT_METHOD_CHOICES = (
		('bank_transfer', 'Chuyển khoản ngân hàng'),
		('cash', 'Tiền mặt'),
		('check', 'Séc'),
	)

	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

	def __str__(self):
		return f"{self.code} - {self.payroll.name}"


class PayrollPaymentDetail(models.Model):
    payment = models.ForeignKey(PayrollPayment, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Chờ xử lý'), ('paid', 'Đã thanh toán')],
        default='pending'
    )
    payment_date = models.DateField()
    reference = models.CharField(max_length=100, blank=True, null=True)  # <-- thêm dòng này

    def __str__(self):
        return f"{self.employee.full_name} - {self.payment.code}"



class Payslip(models.Model):
	code = models.CharField(max_length=50, unique=True)
	payroll_detail = models.ForeignKey(PayrollDetail, on_delete=models.CASCADE)
	issue_date = models.DateField()
	is_sent = models.BooleanField(default=False)
	sent_date = models.DateField(null=True, blank=True)
	is_viewed = models.BooleanField(default=False)
	viewed_date = models.DateField(null=True, blank=True)

	def __str__(self):
		return self.code

class Contract(models.Model):
	CONTRACT_TYPES = (
		('probation', 'Thử việc'),
		('definite', 'Xác định thời hạn'),
		('indefinite', 'Không xác định thời hạn'),
	)

	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='contracts')
	contract_type = models.CharField("Loại hợp đồng", max_length=20, choices=CONTRACT_TYPES)
	start_date = models.DateField("Ngày bắt đầu")
	end_date = models.DateField("Ngày kết thúc", null=True, blank=True)
	position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, related_name='payroll_contracts')
	basic_salary = models.DecimalField("Lương cơ bản", max_digits=12, decimal_places=0)
	insurance_salary = models.DecimalField("Lương đóng bảo hiểm", max_digits=12, decimal_places=0, default=0)
	is_active = models.BooleanField("Đang hiệu lực", default=True)

	def __str__(self):
		return f"{self.employee.full_name} - {self.get_contract_type_display()}"


class WorkHistory(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='work_histories')
	company = models.CharField("Công ty", max_length=100)
	position = models.CharField("Vị trí", max_length=100)
	start_date = models.DateField("Ngày bắt đầu")
	end_date = models.DateField("Ngày kết thúc", null=True, blank=True)
	description = models.TextField("Mô tả công việc", blank=True, null=True)

	def __str__(self):
		return f"{self.employee.full_name} - {self.company}"


class SalaryHistory(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='salary_histories')
	effective_date = models.DateField("Ngày hiệu lực")
	old_salary = models.DecimalField("Lương cũ", max_digits=12, decimal_places=0)
	new_salary = models.DecimalField("Lương mới", max_digits=12, decimal_places=0)
	reason = models.TextField("Lý do thay đổi")

	def __str__(self):
		return f"{self.employee.full_name} - {self.effective_date}"


class Position(models.Model):
	code = models.CharField("Mã vị trí", max_length=20, unique=True)
	name = models.CharField("Tên vị trí", max_length=100)
	department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='payroll_positions')
	is_active = models.BooleanField("Đang hoạt động", default=True)

	def __str__(self):
		return f"{self.code} - {self.name}"

class Department(models.Model):
	code = models.CharField("Mã đơn vị", max_length=20, unique=True)
	name = models.CharField("Tên đơn vị", max_length=100)
	is_active = models.BooleanField("Đang hoạt động", default=True)

	def __str__(self):
		return f"{self.code} - {self.name}"