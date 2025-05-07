from django.db import models
import datetime
from django.utils.translation import gettext_lazy as _


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

    # Thông tin cơ bản
    code = models.CharField(_("Mã nhân viên"), max_length=20, unique=True)
    first_name = models.CharField(_("Tên"), max_length=50)
    last_name = models.CharField(_("Họ"), max_length=50)
    full_name = models.CharField(_("Họ và tên"), max_length=100, blank=True)
    gender = models.CharField(_("Giới tính"), max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(_("Ngày sinh"))
    id_number = models.CharField(_("Số CMND/CCCD"), max_length=20, blank=True, null=True)

    # Thông tin liên hệ
    phone = models.CharField(_("Số điện thoại"), max_length=20)
    email = models.EmailField(_("Email"), blank=True, null=True)
    address = models.CharField(_("Địa chỉ"), max_length=255, blank=True, null=True)

    # Thông tin công việc
    position = models.ForeignKey('Position', on_delete=models.SET_NULL, null=True, verbose_name=_("Vị trí công việc"))
    join_date = models.DateField(_("Ngày vào làm"))
    is_active = models.BooleanField(_("Đang làm việc"), default=True)

    # Thông tin bằng cấp
    education_level = models.CharField(_("Trình độ học vấn"), max_length=20, choices=EDUCATION_LEVEL_CHOICES,
                                       blank=True, null=True)
    degree = models.CharField(_("Bằng cấp"), max_length=100, blank=True, null=True)
    major = models.CharField(_("Chuyên ngành"), max_length=100, blank=True, null=True)

    # Thông tin lương
    basic_salary = models.DecimalField(_("Lương cơ bản"), max_digits=12, decimal_places=0, blank=True, null=True)

    # Ảnh đại diện
    photo = models.ImageField(_("Ảnh"), upload_to='employees/', blank=True, null=True)

    # Thời gian tạo và cập nhật
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Luôn cập nhật full_name mỗi khi lưu, không chỉ khi nó trống
        self.full_name = f"{self.last_name} {self.first_name}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.full_name}"

    class Meta:
        verbose_name = _("Nhân viên")
        verbose_name_plural = _("Nhân viên")
        ordering = ['code']

class Contract(models.Model):
    CONTRACT_TYPES = (
        ('probation', 'Thử việc'),
        ('definite', 'Xác định thời hạn'),
        ('indefinite', 'Không xác định thời hạn'),
    )

    WORK_FORMS = (
        ('fulltime', 'Toàn thời gian'),
        ('parttime', 'Bán thời gian'),
        ('remote', 'Từ xa'),
        ('hybrid', 'Kết hợp'),
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='contracts', verbose_name="Nhân viên")
    contract_number = models.CharField("Số hợp đồng", max_length=20, unique=True)
    contract_name = models.CharField("Tên hợp đồng", max_length=200, blank=True, null=True)
    contract_type = models.CharField("Loại hợp đồng", max_length=20, choices=CONTRACT_TYPES)
    work_form = models.CharField("Hình thức làm việc", max_length=20, choices=WORK_FORMS, default='fulltime',
                                 blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='department_contracts', verbose_name="Đơn vị ký hợp đồng")
    start_date = models.DateField("Ngày có hiệu lực")
    end_date = models.DateField("Ngày kết thúc", null=True, blank=True)
    sign_date = models.DateField("Ngày ký", null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, related_name='employee_contracts',
                                 verbose_name="Vị trí công việc")
    basic_salary = models.DecimalField("Lương cơ bản", max_digits=12, decimal_places=0)
    insurance_salary = models.DecimalField("Lương đóng bảo hiểm", max_digits=12, decimal_places=0, default=0)
    is_active = models.BooleanField("Đang hiệu lực", default=True)
    created_at = models.DateTimeField("Ngày tạo", auto_now_add=True)
    updated_at = models.DateTimeField("Ngày cập nhật", auto_now=True)

    def __str__(self):
        return f"{self.contract_number} - {self.employee.full_name}"

    class Meta:
        verbose_name = "Hợp đồng"
        verbose_name_plural = "Hợp đồng"
        ordering = ['-start_date']

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