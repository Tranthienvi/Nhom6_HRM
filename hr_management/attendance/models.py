from django.db import models
from employees.models import Employee, Position


class WorkShift(models.Model):
	name = models.CharField("Tên ca", max_length=100)
	start_time = models.TimeField("Giờ bắt đầu")
	end_time = models.TimeField("Giờ kết thúc")
	break_time = models.PositiveIntegerField("Thời gian nghỉ (phút)", default=0)

	def __str__(self):
		return f"{self.name} ({self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')})"


class AttendanceSheet(models.Model):
	name = models.CharField("Tên bảng chấm công", max_length=100)
	month = models.PositiveIntegerField("Tháng")
	year = models.PositiveIntegerField("Năm")
	positions = models.ManyToManyField(Position, verbose_name="Vị trí áp dụng")
	created_at = models.DateTimeField("Ngày tạo", auto_now_add=True)

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

	def __str__(self):
		return f"{self.employee.full_name} - {self.date} - {self.get_status_display()}"
