from django.db import models
import datetime


class Department(models.Model):
	code = models.CharField("Mã đơn vị", max_length=20, unique=True)
	name = models.CharField("Tên đơn vị", max_length=100)
	is_active = models.BooleanField("Đang hoạt động", default=True)

	def __str__(self):
		return f"{self.code} - {self.name}"


class Position(models.Model):
	code = models.CharField("Mã vị trí", max_length=20, unique=True)
	name = models.CharField("Tên vị trí", max_length=100)
	department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employee_positions')
	is_active = models.BooleanField("Đang hoạt động", default=True)

	def __str__(self):
		return f"{self.code} - {self.name}"


class Employee(models.Model):
    GENDER_CHOICES = [
        ('M', 'Nam'),
        ('F', 'Nữ'),
        ('O', 'Khác'),
    ]

    LABOR_STATUS_CHOICES = [
        ('working', 'Đang làm việc'),
        ('retired', 'Đã nghỉ việc'),
    ]

    EMPLOYMENT_TYPE_CHOICES = [
        ('official', 'Chính thức'),
        ('probation', 'Thử việc'),
        ('intern', 'Học việc'),
        ('temporary', 'Tạm thời'),
        ('other', 'Khác'),
    ]

    CONTRACT_TYPE_CHOICES = [
        ('probation', 'Thử việc'),
        ('definite', 'Hợp đồng xác định thời hạn'),
        ('indefinite', 'Hợp đồng không xác định thời hạn'),
        ('seasonal', 'Hợp đồng mùa vụ'),
        ('service', 'Hợp đồng dịch vụ'),
    ]

    code = models.CharField("Mã nhân viên", max_length=20, unique=True)
    first_name = models.CharField("Tên", max_length=50)
    last_name = models.CharField("Họ", max_length=50)
    full_name = models.CharField("Họ và tên", max_length=100)
    gender = models.CharField("Giới tính", max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField("Ngày sinh")
    id_number = models.CharField("Số CMND/CCCD", max_length=20, unique=True)
    phone = models.CharField("Số điện thoại", max_length=15)
    email = models.EmailField("Email", max_length=100)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, related_name='employees', verbose_name="Vị trí công việc")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='employees')
    join_date = models.DateField("Ngày vào làm")
    is_active = models.BooleanField("Đang làm việc", default=True)
    photo = models.ImageField("Ảnh", upload_to='employees/photos/', blank=True, null=True)

    # Các trường mới bổ sung
    labor_status = models.CharField("Trạng thái lao động", max_length=20, choices=LABOR_STATUS_CHOICES, default='working')
    employment_type = models.CharField("Tính chất lao động", max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, default='official')
    contract_type = models.CharField("Loại hợp đồng", max_length=20, choices=CONTRACT_TYPE_CHOICES, null=True, blank=True)
    dependents = models.IntegerField("Số người phụ thuộc", default=0)

    def __str__(self):
        return f"{self.code} - {self.full_name}"

        def save(self, *args, **kwargs):
	        super().save(*args, **kwargs)

        def seniority(self):
	        today = datetime.date.today()
	        return today.year - self.join_date.year


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
	position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, related_name='employee_contracts')
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
