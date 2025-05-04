# payroll/models.py
from django.db import models

class PayrollTemplate(models.Model):
    name = models.CharField(max_length=100)
    positions = models.ManyToManyField('employees.Position', blank=True)
    is_active = models.BooleanField(default=True)  # Trường is_active để kiểm tra tính hoạt động

    def __str__(self):
        return self.name

class PayrollComponent(models.Model):
    name = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=2)  # Adjust type as needed
    formula = models.CharField(max_length=255, blank=True)  # Adjust type as needed
    component_type = models.CharField(max_length=50)  # Adjust type as needed

    def __str__(self):
        return self.name

class Payroll(models.Model):

    year = models.IntegerField()
    month = models.IntegerField()
    positions = models.ManyToManyField('employees.Position', blank=True)
    attendance_sheet = models.ForeignKey('attendance.AttendanceSheet', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  # Trường is_active
    name = models.CharField(max_length=255)  # Thêm nếu thiếu
    template = models.ForeignKey(PayrollTemplate, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.month}/{self.year}'

class PayrollDetail(models.Model):
    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE)
    employee = models.ForeignKey('employees.Employee', on_delete=models.CASCADE)
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    actual_workdays = models.IntegerField()
    total_income = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Detail for {self.employee.name} - {self.payroll.year}/{self.payroll.month}'
