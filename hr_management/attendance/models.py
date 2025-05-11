from django.db import models
from employees.models import Employee, Position

from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from datetime import date

class AttendanceSheet(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Bản nháp'),
        ('active', 'Đang hoạt động'),
        ('closed', 'Đã đóng'),
        ('transferred', 'Đã chuyển tính lương'),
    ]

    name = models.CharField("Tên bảng chấm công", max_length=100)
    month = models.PositiveIntegerField("Tháng")
    year = models.PositiveIntegerField("Năm")
    positions = models.ManyToManyField(Position, related_name='attendance_sheets', verbose_name="Vị trí áp dụng")
    standard_workdays = models.PositiveIntegerField("Số công chuẩn", default=22)
    paid_leave = models.PositiveIntegerField("Nghỉ có phép", default=0)
    unpaid_leave = models.PositiveIntegerField("Nghỉ không phép", default=0)
    policy_leave = models.PositiveIntegerField("Công nghỉ chế độ", default=0)
    attendance_type = models.CharField("Hình thức chấm công", max_length=50, default="Theo ca")
    created_at = models.DateTimeField("Ngày tạo", auto_now_add=True)
    status = models.CharField("Trạng thái", max_length=20, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return f"{self.name} - {self.month}/{self.year}"

    def get_month_year_display(self):
        return f"{self.month}/{self.year}"


class AttendanceRecord(models.Model):
    STATUS_CHOICES = [
        ('present', 'Có mặt'),
        ('absent', 'Vắng mặt'),
        ('late', 'Đi muộn'),
        ('early', 'Về sớm'),
        ('leave', 'Nghỉ phép'),
    ]
    ATTENDANCE_TYPE_CHOICES = (
                ('shift', 'Theo ca'),
                ('daily', 'Theo ngày'),
            )
    name = models.CharField("Tên bảng chấm công", max_length=100)
    sheet = models.ForeignKey(AttendanceSheet, on_delete=models.CASCADE, related_name='records')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance_records')
    attendance_date = models.DateField("Ngày", null=True)
    status = models.CharField("Trạng thái", max_length=20, choices=STATUS_CHOICES, default='present')
    check_in = models.TimeField("Giờ vào", null=True, blank=True)
    check_out = models.TimeField("Giờ ra", null=True, blank=True)
    work_hours = models.DecimalField("Số giờ làm việc", max_digits=5, decimal_places=2, default=0)
    overtime = models.DecimalField("Giờ làm thêm", max_digits=5, decimal_places=2, default=0)
    note = models.CharField("Ghi chú", max_length=200, blank=True)

    # Bổ sung default
    start_date = models.DateField(verbose_name="Ngày bắt đầu", default=date.today)
    end_date = models.DateField(verbose_name="Ngày kết thúc", default=date.today)

    # Giả sử ATTENDANCE_TYPE_CHOICES có ('default', 'Bình thường'), thì bạn dùng 'default'
    attendance_type = models.CharField(
        max_length=20,
        choices=ATTENDANCE_TYPE_CHOICES,
        verbose_name="Hình thức chấm công",
        default='default'  # hoặc giá trị mặc định phù hợp trong ATTENDANCE_TYPE_CHOICES
    )

    # Bạn cần tạo một bản ghi Position trước để dùng default ID
    positions = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        verbose_name="Vị trí áp dụng",
        default=1  # Cần đảm bảo Position với ID = 1 tồn tại
    )
    # work_shifts = models.ManyToManyField(WorkShift, blank=True, verbose_name="Ca làm việc")
    apply_to_all_shifts = models.BooleanField(default=False, verbose_name="Chọn tất cả ca")


    def __str__(self):
        return f"{self.employee.full_name} - {self.date} - {self.get_status_display()}"

class WorkShift(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên ca làm việc")
    code = models.CharField(max_length=20, verbose_name="Mã ca")
    start_time = models.TimeField(verbose_name="Giờ bắt đầu ca")
    check_in_start = models.TimeField(verbose_name="Chấm vào - Từ")
    check_in_end = models.TimeField(verbose_name="Chấm vào - Đến")
    end_time = models.TimeField(verbose_name="Giờ kết thúc ca")
    check_out_start = models.TimeField(verbose_name="Chấm ra - Từ")
    check_out_end = models.TimeField(verbose_name="Chấm ra - Đến")
    has_break = models.BooleanField(default=False, verbose_name="Có nghỉ giữa ca")
    work_hours = models.FloatField(default=0, verbose_name="Giờ công")
    work_days = models.FloatField(default=1, verbose_name="Ngày công")
    normal_day_coefficient = models.FloatField(default=1, verbose_name="Hệ số ngày thường")
    rest_day_coefficient = models.FloatField(default=2, verbose_name="Hệ số ngày nghỉ")
    holiday_coefficient = models.FloatField(default=3, verbose_name="Hệ số ngày lễ")
    deduct_if_no_check_in = models.BooleanField(default=False, verbose_name="Trừ công nếu không có giờ vào")
    deduct_if_no_check_out = models.BooleanField(default=False, verbose_name="Trừ công nếu không có giờ ra")
    apply_to_all = models.BooleanField(default=False, verbose_name="Toàn đơn vị")
    employees = models.ManyToManyField(
        'employees.Employee',
        blank=True,
        verbose_name="Danh sách nhân viên"
    )

    def __str__(self):
        return f"{self.name} ({self.start_time} - {self.end_time})"

    class Meta:
        verbose_name = "Ca làm việc"
        verbose_name_plural = "Các ca làm việc"

# class AttendanceRecord(models.Model):
#     ATTENDANCE_TYPE_CHOICES = (
#         ('shift', 'Theo ca'),
#         ('daily', 'Theo ngày'),
#     )
#
#     name = models.CharField(max_length=200, verbose_name="Tên bảng chấm công")
#     start_date = models.DateField(verbose_name="Ngày bắt đầu")
#     end_date = models.DateField(verbose_name="Ngày kết thúc")
#     attendance_type = models.CharField(max_length=20, choices=ATTENDANCE_TYPE_CHOICES, verbose_name="Hình thức chấm công")
#     positions = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name="Vị trí áp dụng")
#     apply_to_all_shifts = models.BooleanField(default=False, verbose_name="Chọn tất cả ca")
#     work_shifts = models.ManyToManyField(WorkShift, blank=True, verbose_name="Ca làm việc")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = "Bảng chấm công chi tiết"
#         verbose_name_plural = "Các bảng chấm công chi tiết"
#         ordering = ['-start_date']

class DailyAttendance(models.Model):
    ATTENDANCE_STATUS_CHOICES = (
        ('not_absent', 'Không nghỉ'),
        ('permitted_absence', 'Nghỉ có phép'),
        ('unpermitted_absence', 'Nghỉ không phép'),
        ('regime_absence', 'Nghỉ theo chế độ'),
    )

    attendance_record = models.ForeignKey(AttendanceRecord, on_delete=models.CASCADE, related_name='daily_attendances', verbose_name="Bảng chấm công")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Nhân viên")
    date = models.DateField(verbose_name="Ngày chấm công")
    paid_work_days = models.FloatField(default=1, verbose_name="Số công hưởng lương")
    actual_work_days = models.FloatField(default=1, verbose_name="Số công đi làm thực tế")
    check_in_time = models.TimeField(null=True, blank=True, verbose_name="Giờ vào")
    check_out_time = models.TimeField(null=True, blank=True, verbose_name="Giờ ra")
    attendance_status = models.CharField(max_length=20, choices=ATTENDANCE_STATUS_CHOICES, default='not_absent', verbose_name="Nghỉ")
    work_shift = models.ForeignKey(WorkShift, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Ca làm việc")

    def __str__(self):
        return f"{self.employee.full_name} - {self.date} - {self.attendance_record.name}"

    class Meta:
        verbose_name = "Chấm công hàng ngày"
        verbose_name_plural = "Chấm công hàng ngày"
        unique_together = ('attendance_record', 'employee', 'date')  # Đảm bảo không có bản ghi trùng lặp

class AttendanceSummary(models.Model):
    name = models.CharField(max_length=200, verbose_name="Tên bảng chấm công tổng hợp")
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name="Vị trí áp dụng")
    attendance_records = models.ManyToManyField(AttendanceRecord, verbose_name="Danh sách bảng chấm công chi tiết")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Bảng chấm công tổng hợp"
        verbose_name_plural = "Các bảng chấm công tổng hợp"
        ordering = ['-created_at']

    @property
    def date_range(self):
        records = self.attendance_records.all()
        if records:
            start_date = min(record.start_date for record in records)
            end_date = max(record.end_date for record in records)
            return f"{start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}"
        return "N/A"