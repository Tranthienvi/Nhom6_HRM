# from django.db import models
# from employees.models import Employee, Position
# from datetime import datetime
#
# class WorkShift(models.Model):
# 	name = models.CharField("Tên ca", max_length=100)
# 	start_time = models.TimeField("Giờ bắt đầu")
# 	end_time = models.TimeField("Giờ kết thúc")
# 	break_time = models.PositiveIntegerField("Thời gian nghỉ (phút)", default=0)
#
# 	def __str__(self):
# 		return f"{self.name} ({self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')})"
#
# 	class Meta:
# 		verbose_name = "Ca làm việc"
# 		verbose_name_plural = "Ca làm việc"
# 		ordering = ['start_time']
#
#
# class AttendanceSheet(models.Model):
# 	name = models.CharField("Tên bảng chấm công", max_length=100)
# 	month = models.PositiveIntegerField("Tháng")
# 	year = models.PositiveIntegerField("Năm")
# 	positions = models.ManyToManyField(Position, verbose_name="Vị trí áp dụng")
# 	created_at = models.DateTimeField("Ngày tạo", default=datetime.now)
#
# 	def __str__(self):
# 		return f"{self.name} - {self.month}/{self.year}"
#
# 	class Meta:
# 		verbose_name = "Bảng chấm công"
# 		verbose_name_plural = "Bảng chấm công"
# 		ordering = ['-year', '-month']
#
#
# class AttendanceRecord(models.Model):
# 	STATUS_CHOICES = (
# 		('present', 'Có mặt'),
# 		('absent', 'Vắng mặt'),
# 		('late', 'Đi muộn'),
# 		('leave', 'Nghỉ phép'),
# 	)
#
# 	sheet = models.ForeignKey(AttendanceSheet, on_delete=models.CASCADE, related_name='records',
# 	                          verbose_name="Bảng chấm công")
# 	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Nhân viên")
# 	date = models.DateField("Ngày")
# 	status = models.CharField("Trạng thái", max_length=10, choices=STATUS_CHOICES)
# 	check_in = models.TimeField("Giờ vào", null=True, blank=True)
# 	check_out = models.TimeField("Giờ ra", null=True, blank=True)
# 	working_hours = models.DecimalField("Số giờ làm việc", max_digits=4, decimal_places=1, default=0)
# 	note = models.CharField("Ghi chú", max_length=200, blank=True, null=True)
#
# 	def __str__(self):
# 		return f"{self.employee.full_name} - {self.date} - {self.get_status_display()}"
#
# 	class Meta:
# 		verbose_name = "Bản ghi chấm công"
# 		verbose_name_plural = "Bản ghi chấm công"
# 		ordering = ['-date']
# 		unique_together = ['sheet', 'employee', 'date']
from django.db import models
from employees.models import Employee, Position
from django.utils.translation import gettext_lazy as _

class WorkShift(models.Model):
	name = models.CharField("Tên ca", max_length=100)
	start_time = models.TimeField("Giờ bắt đầu")
	end_time = models.TimeField("Giờ kết thúc")
	break_time = models.PositiveIntegerField("Thời gian nghỉ (phút)", default=0)

	# Các trường mới bổ sung
	working_hours = models.DecimalField("Giờ công", max_digits=4, decimal_places=2, default=8.0)
	normal_day_coefficient = models.DecimalField("Hệ số ngày thường", max_digits=3, decimal_places=2, default=1.0)
	rest_day_coefficient = models.DecimalField("Hệ số ngày nghỉ", max_digits=3, decimal_places=2, default=1.5)
	holiday_coefficient = models.DecimalField("Hệ số ngày lễ", max_digits=3, decimal_places=2, default=2.0)
	is_active = models.BooleanField("Đang sử dụng", default=True)

	def __str__(self):
		return f"{self.name} ({self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')})"


class AttendanceSheet(models.Model):
	ATTENDANCE_TYPE_CHOICES = (
		('daily', 'Theo ngày'),
		('shift', 'Theo ca'),
	)

	name = models.CharField("Tên bảng chấm công", max_length=100)
	month = models.PositiveIntegerField("Tháng")
	year = models.PositiveIntegerField("Năm")
	positions = models.ManyToManyField(Position, verbose_name="Vị trí áp dụng")
	created_at = models.DateTimeField("Ngày tạo", auto_now_add=True)

	# Các trường mới bổ sung
	attendance_type = models.CharField("Hình thức chấm công", max_length=10, choices=ATTENDANCE_TYPE_CHOICES,
	                                   default='daily')
	standard_workdays = models.PositiveIntegerField("Số công chuẩn", default=22)
	paid_leave = models.PositiveIntegerField("Công nghỉ chế độ", default=0)
	approved_leave = models.PositiveIntegerField("Nghỉ có phép", default=0)
	unapproved_leave = models.PositiveIntegerField("Nghỉ không phép", default=0)
	is_transferred = models.BooleanField("Đã chuyển tính lương", default=False)

	def __str__(self):
		return f"{self.name} - {self.month}/{self.year}"


class AttendanceRecord(models.Model):
	STATUS_CHOICES = (
		('present', 'Có mặt'),
		('absent', 'Vắng mặt'),
		('late', 'Đi muộn'),
		('leave', 'Nghỉ phép'),
	)

	sheet = models.ForeignKey(AttendanceSheet, on_delete=models.CASCADE, related_name='records')
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
	date = models.DateField("Ngày")
	status = models.CharField("Trạng thái", max_length=10, choices=STATUS_CHOICES)
	check_in = models.TimeField("Giờ vào", null=True, blank=True)
	check_out = models.TimeField("Giờ ra", null=True, blank=True)
	working_hours = models.DecimalField("Số giờ làm việc", max_digits=4, decimal_places=1, default=0)
	note = models.CharField("Ghi chú", max_length=200, blank=True, null=True)

	# Trường mới bổ sung
	work_shift = models.ForeignKey(WorkShift, on_delete=models.SET_NULL, null=True, blank=True,
	                               verbose_name="Ca làm việc")

	def __str__(self):
		return f"{self.employee.full_name} - {self.date} - {self.get_status_display()}"

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

class PayrollComponent(models.Model):
    # Các trường trong bảng lương
    name = models.CharField(("Tên thành phần"), max_length=100)
    amount = models.DecimalField(_("Số tiền"), max_digits=12, decimal_places=2)
    component_type = models.CharField(_("Loại thành phần"), max_length=50)  # Ví dụ: Lương cơ bản, thưởng,...
    is_active = models.BooleanField(_("Kích hoạt"), default=True)

    payroll_template = models.ForeignKey(
        'PayrollTemplate', on_delete=models.CASCADE, related_name='components', verbose_name=_("Mẫu bảng lương")
    )

    def __str__(self):
        return self.name