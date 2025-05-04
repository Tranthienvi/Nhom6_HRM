# employees/models.py

from django.db import models

# Department Model
class Department(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# Position Model
class Position(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# Employee Model
class Employee(models.Model):
    # Employee fields
    code = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    id_number = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    position = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    join_date = models.DateField()
    photo = models.ImageField(upload_to='employee_photos/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Contract Model
class Contract(models.Model):
    # Contract fields
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='contracts')
    contract_type = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    position = models.CharField(max_length=50)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Contract for {self.employee.first_name} {self.employee.last_name}"

# WorkHistory Model
class WorkHistory(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Work history of {self.employee} ({self.start_date} to {self.end_date if self.end_date else 'Present'})"

# SalaryHistory Model
class SalaryHistory(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Salary history of {self.employee} from {self.start_date} to {self.end_date if self.end_date else 'Present'}"
