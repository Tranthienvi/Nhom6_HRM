from django.db import models
import datetime
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal

class Position(models.Model):
    POSITION_CHOICES = [
        ('GV', 'Giảng viên'),
        ('TG', 'Trợ giảng'),
        ('NVNS', 'Nhân viên nhân sự'),
        ('NVTV', 'Nhân viên tư vấn'),
        ('QL', 'Quản lý'),
    ]

    code = models.CharField("Mã vị trí", max_length=20, unique=True)
    name = models.CharField("Tên vị trí công vi���c", max_length=50)
    is_active = models.BooleanField("Đang hoạt động", default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Đảm bảo chỉ có 5 vị trí được định nghĩa
        if not self.pk and Position.objects.count() >= 5:
            raise ValidationError("Chỉ được phép có tối đa 5 vị trí công việc")
        super().save(*args, **kwargs)


class Employee(models.Model):
    GENDER_CHOICES = (
        ('male', 'Nam'),
        ('female', 'Nữ'),
        ('other', 'Khác'),
    )

    EDUCATION_LEVEL_CHOICES = (
        ('high_school', 'Trung học phổ thông'),
        ('college', 'Cao đẳng'),
        ('university', 'Đại học'),
        ('master', 'Thạc sĩ'),
        ('phd', 'Tiến sĩ'),
    )


    EMPLOYMENT_TYPE_CHOICES = (
        ('full_time', 'Toàn thời gian'),
        ('part_time', 'Bán thời gian'),
        ('intern', 'Thực tập'),

    )

    # EMPLOYMENT_TYPE_CHOICES = [
    #     ('official', 'Chính thức'),
    #     ('probation', 'Thử việc'),
    #     ('intern', 'Học việc'),
    #     ('temporary', 'Tạm thời'),
    #     ('other', 'Khác'),
    # ]

    LABOR_STATUS_CHOICES = (
        ('working', 'Đang làm việc'),
        ('resigned', 'Đã nghỉ việc'),
        ('maternity_leave', 'Nghỉ thai sản'),
        ('on_leave', 'Đang nghỉ phép'),
    )



    IS_ACTIVE_CHOICES = [
        ('active', 'Đang làm việc'),
        ('inactive', 'Đã nghỉ việc'),
    ]


    # Thông tin cơ bản
    code = models.CharField(_("Mã nhân viên"), max_length=20, unique=True)
    full_name = models.CharField(_("Họ và tên"), max_length=100, blank=True)
    gender = models.CharField(_("Giới tính"), max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(_("Ngày sinh"))
    id_number = models.CharField(_("Số CMND/CCCD"), max_length=20, blank=True, null=True)

    # Thông tin liên hệ
    phone = models.CharField(_("Số điện thoại"), max_length=20)
    email = models.EmailField(_("Email"), blank=True, null=True)
    address = models.CharField(_("Địa chỉ"), max_length=255, blank=True, null=True)

    # Thông tin công việc
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name="Vị trí công việc")
    join_date = models.DateField(_("Ngày vào làm"))
    is_active = models.CharField("Trạng thái làm việc", max_length=10, choices=IS_ACTIVE_CHOICES, default='active')

    # Ảnh đại diện
    photo = models.ImageField(_("Ảnh"), upload_to='employees/', blank=True, null=True)

    employment_type = models.CharField(_("Loại công việc"), max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, blank=True,
                                       null=True)

    # Thông tin lương và thuế
    basic_salary = models.DecimalField("Lương cơ bản", max_digits=12, decimal_places=0, default=0, null=True,
                                       blank=True)
    salary_rate = models.DecimalField("Tỉ lệ hưởng lương", max_digits=5, decimal_places=2, default=100, null=True,
                                      blank=True)



    # Thông tin bằng cấp
    education_level = models.CharField(_("Trình độ học vấn"), max_length=20, choices=EDUCATION_LEVEL_CHOICES,
                                       blank=True, null=True)
    degree = models.CharField(_("Bằng cấp"), max_length=100, blank=True, null=True)
    major = models.CharField(_("Chuyên ngành"), max_length=100, blank=True, null=True)


    # Thông tin bổ sung mới
    dependents = models.PositiveIntegerField(_("Số người phụ thuộc"), default=0)
    labor_status = models.CharField(_("Tình trạng lao động"), max_length=20, choices=LABOR_STATUS_CHOICES, default='working')
    personal_tax = models.DecimalField("Thuế TNCN (%)", max_digits=5, decimal_places=2, default=0, null=True,
                                       blank=True)
    deduction = models.DecimalField("Khấu trừ", max_digits=12, decimal_places=0, default=0, null=True, blank=True)
    performance_bonus = models.DecimalField("Thưởng hiệu suất", max_digits=12, decimal_places=0, default=0, null=True,
                                            blank=True)

    # Thời gian tạo và cập nhật
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.full_name}"

    def clean(self):
        # Kiểm tra ngày sinh không được lớn hơn ngày hiện tại
        if self.date_of_birth and self.date_of_birth > timezone.now().date():
            raise ValidationError({'date_of_birth': 'Ngày sinh không thể lớn hơn ngày hiện tại'})

        # Kiểm tra ngày vào làm không được nhỏ hơn ngày sinh
        if self.date_of_birth and self.join_date and self.join_date < self.date_of_birth:
            raise ValidationError({'join_date': 'Ngày vào làm không thể nhỏ hơn ngày sinh'})

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