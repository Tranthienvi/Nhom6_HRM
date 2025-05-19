from django.contrib import admin
from .models import Position, Employee, Contract


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
	list_display = ('name', 'description')
	search_fields = ('name',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
	list_display = ('code', 'full_name', 'position', 'phone', 'is_active')
	list_filter = ('position', 'is_active', 'gender')
	search_fields = ('code', 'first_name', 'last_name', 'phone', 'email')
	fieldsets = (
		('Thông tin cơ bản', {
			'fields': ('code', 'first_name', 'last_name', 'gender', 'date_of_birth', 'id_number', 'photo')
		}),
		('Thông tin liên hệ', {
			'fields': ('phone', 'email', 'address')
		}),
		('Thông tin công việc', {
			'fields': ('position', 'join_date', 'is_active')
		}),
		('Thông tin học vấn', {
			'fields': ('education_level', 'degree', 'major')
		}),
		('Thông tin lương', {
			'fields': ('basic_salary',)
		}),
	)

	def full_name(self, obj):
		return obj.full_name

	full_name.short_description = 'Họ và tên'


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
	list_display = ('contract_number', 'employee', 'contract_type', 'position', 'start_date', 'end_date', 'status')
	list_filter = ('contract_type', 'status', 'position')
	search_fields = ('contract_number', 'employee__full_name', 'employee__code')
	date_hierarchy = 'start_date'

	fieldsets = (
		('Thông tin cơ bản', {
			'fields': ('employee', 'contract_number', 'contract_type', 'position', 'status')
		}),
		('Thời gian', {
			'fields': ('start_date', 'end_date', 'signed_date')
		}),
		('Thông tin lương', {
			'fields': ('basic_salary', 'allowance', 'insurance_salary')
		}),
		('Thông tin khác', {
			'fields': ('notes', 'file')
		}),
	)
