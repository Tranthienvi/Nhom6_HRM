from django.contrib import admin
from .models import  Position, Employee, WorkHistory, SalaryHistory

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'is_active')
    search_fields = ('code', 'name')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('code', 'full_name', 'position', 'phone', 'is_active')
    search_fields = ('code', 'full_name', 'phone', 'email')
    list_filter = ('position', 'is_active', 'gender', 'education_level')
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('code', 'full_name', 'gender', 'date_of_birth', 'photo')
        }),
        ('Thông tin liên hệ', {
            'fields': ('phone', 'email', 'id_number', 'address')
        }),
        ('Thông tin công việc', {
            'fields': ('position', 'join_date', 'is_active')
        }),
        ('Thông tin bằng cấp', {
            'fields': ('education_level', 'degree', 'major')
        }),
        ('Thông tin lương', {
            'fields': ('basic_salary',)
        }),
    )

@admin.register(WorkHistory)
class WorkHistoryAdmin(admin.ModelAdmin):
    list_display = ('employee', 'company', 'position', 'start_date', 'end_date')
    search_fields = ('employee__full_name', 'company', 'position')

@admin.register(SalaryHistory)
class SalaryHistoryAdmin(admin.ModelAdmin):
    list_display = ('employee', 'effective_date', 'old_salary', 'new_salary')
    search_fields = ('employee__full_name',)
    list_filter = ('effective_date',)