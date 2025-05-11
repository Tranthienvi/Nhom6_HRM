from django.db import models
from employees.models import Employee, Position, WorkHistory, SalaryHistory
from attendance.models import AttendanceSheet
from django.utils import timezone
from decimal import Decimal



class PayrollTemplate(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="payroll_positions",
                                 verbose_name="Vị trí áp dụng")
    salary = models.DecimalField(max_digits=12, decimal_places=2)
    bonus = models.DecimalField(max_digits=12, decimal_places=2)
    deductions = models.DecimalField(max_digits=12, decimal_places=2)
    effective_date = models.DateField()


    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField("Ngày cập nhật", auto_now=True)

    def __str__(self):
        return self.name


class PayrollComponent(models.Model):
	COMPONENT_TYPES = (
		('allowance', 'Phụ cấp'),
		('bonus', 'Thưởng'),
		('deduction', 'Khấu trừ'),
		('tax', 'Thuế'),
	)

	name = models.CharField("Tên thành phần", max_length=100)
	code = models.CharField("Mã thành phần", max_length=20)
	component_type = models.CharField("Loại thành phần", max_length=20, choices=COMPONENT_TYPES)
	amount = models.DecimalField("Số tiền", max_digits=12, decimal_places=0, default=0)
	is_percentage = models.BooleanField("Là phần trăm", default=False)
	is_taxable = models.BooleanField("Chịu thuế", default=False)
	is_active = models.BooleanField("Đang hoạt động", default=True)

	created_at = models.DateTimeField("Ngày tạo", auto_now_add=True)
	updated_at = models.DateTimeField("Ngày cập nhật", auto_now=True)

	def __str__(self):
		return self.name

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
	payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE, related_name="details")
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="payroll_details")

	# Dữ liệu từ bảng chấm công
	standard_workdays = models.PositiveIntegerField("Số công chuẩn", default=22)
	actual_workdays = models.DecimalField("Số công thực tế", max_digits=5, decimal_places=1, default=0)
	paid_leave = models.DecimalField("Nghỉ có phép", max_digits=5, decimal_places=1, default=0)
	unpaid_leave = models.DecimalField("Nghỉ không phép", max_digits=5, decimal_places=1, default=0)
	policy_leave = models.DecimalField("Công nghỉ chế độ", max_digits=5, decimal_places=1, default=0)

	# Dữ liệu lương
	basic_salary = models.DecimalField("Lương cơ bản", max_digits=12, decimal_places=0, default=0)
	salary_rate = models.DecimalField("Tỉ lệ hưởng lương (%)", max_digits=5, decimal_places=2, default=100)

	# Thuế và giảm trừ
	personal_tax_rate = models.DecimalField("Thuế TNCN (%)", max_digits=5, decimal_places=2, default=0)
	personal_tax_amount = models.DecimalField("Thuế TNCN", max_digits=12, decimal_places=0, default=0)
	personal_deduction = models.DecimalField("Giảm trừ gia cảnh", max_digits=12, decimal_places=0,
	                                         default=11000000)  # 11 triệu mặc định
	dependent_deduction = models.DecimalField("Giảm trừ người phụ thuộc", max_digits=12, decimal_places=0, default=0)
	dependents = models.PositiveIntegerField("Số người phụ thuộc", default=0)

	# Các khoản khấu trừ và thưởng
	deduction = models.DecimalField("Khấu trừ", max_digits=12, decimal_places=0, default=0)
	performance_bonus = models.DecimalField("Thưởng hiệu suất", max_digits=12, decimal_places=0, default=0)

	# Tổng thu nhập và thực lĩnh
	gross_income = models.DecimalField("Tổng thu nhập", max_digits=12, decimal_places=0, default=0)
	net_income = models.DecimalField("Thực lĩnh", max_digits=12, decimal_places=0, default=0)

	overtime_hours = models.DecimalField(max_digits=5, decimal_places=2)
	tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	bonus = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	working_days = models.DecimalField(max_digits=5, decimal_places=2)
	grass_salary = models.DecimalField(max_digits=12, decimal_places=2)
	leave_days = models.DecimalField(max_digits=5, decimal_places=2, default=0)
	allowance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	net_salary = models.DecimalField(max_digits=12, decimal_places=2)
	gross_salary = models.DecimalField(max_digits=12, decimal_places=2)

	created_at = models.DateTimeField("Ngày tạo", auto_now_add=True)
	updated_at = models.DateTimeField("Ngày cập nhật", auto_now=True)

	def __str__(self):
		return f"{self.employee.full_name} - {self.payroll.period.name}"

	def calculate_gross_income(self):
		# Tính lương theo số ngày làm việc thực tế
		workday_ratio = (self.actual_workdays + self.paid_leave + self.policy_leave) / self.standard_workdays
		salary_by_workdays = Decimal(self.basic_salary) * Decimal(workday_ratio)

		# Áp dụng tỉ lệ hưởng lương
		salary_with_rate = salary_by_workdays * (Decimal(self.salary_rate) / Decimal(100))

		# Cộng thêm thưởng hiệu suất
		gross_income = salary_with_rate + Decimal(self.performance_bonus)

		return gross_income

	def calculate_personal_tax(self):
		# Tính tổng thu nhập
		gross_income = self.calculate_gross_income()

		# Tính giảm trừ gia cảnh
		total_deduction = Decimal(self.personal_deduction) + (Decimal(self.dependents) * Decimal(4400000))

		# Tính thu nhập chịu thuế
		taxable_income = max(Decimal(0), gross_income - total_deduction)

		# Tính thuế TNCN
		tax_amount = taxable_income * (Decimal(self.personal_tax_rate) / Decimal(100))

		return tax_amount

	def calculate_net_income(self):
		# Tính tổng thu nhập
		gross_income = self.calculate_gross_income()

		# Tính thuế TNCN
		tax_amount = self.calculate_personal_tax()

		# Tính thực lĩnh
		net_income = gross_income - tax_amount - Decimal(self.deduction)

		return net_income

	def save(self, *args, **kwargs):
		# Tính toán các giá trị trước khi lưu
		self.gross_income = self.calculate_gross_income()
		self.personal_tax_amount = self.calculate_personal_tax()
		self.net_income = self.calculate_net_income()

		# Tính giảm trừ người phụ thuộc
		self.dependent_deduction = Decimal(self.dependents) * Decimal(4400000)

		super().save(*args, **kwargs)

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

    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_pay = models.DecimalField(max_digits=12, decimal_places=2, default=0)


    def __str__(self):
	    return f"{self.employee.full_name} - {self.payroll_data.period.name}"

    def calculate_net_salary(self):
	    gross = self.basic_salary + self.allowance + self.bonus
	    net = gross - self.deduction
	    return net

    def save(self, *args, **kwargs):
	    self.net_salary = self.calculate_net_salary()
	    super().save(*args, **kwargs)

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









