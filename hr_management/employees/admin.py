from django.contrib import admin
from .models import Department, Position, Employee, Contract

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'is_active')
    search_fields = ('code', 'name')
    list_filter = ('is_active',)

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'department', 'is_active')
    search_fields = ('code', 'name')
    list_filter = ('department', 'is_active')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('code', 'full_name', 'position', 'department', 'phone', 'is_active')
    search_fields = ('code', 'full_name', 'phone', 'email')
    list_filter = ('position', 'department', 'is_active', 'gender')
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('code', 'first_name', 'last_name', 'gender', 'date_of_birth', 'photo')
        }),
        ('Thông tin liên hệ', {
            'fields': ('phone', 'email', 'id_number')
        }),
        ('Thông tin công việc', {
            'fields': ('position', 'department', 'join_date', 'is_active')
        }),
    )

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('employee', 'contract_type', 'start_date', 'end_date', 'basic_salary', 'is_active')
    search_fields = ('employee__full_name', 'employee__code')
    list_filter = ('contract_type', 'is_active')
    date_hierarchy = 'start_date'