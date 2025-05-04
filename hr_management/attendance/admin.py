from django.contrib import admin
from .models import WorkShift, AttendanceSheet, AttendanceRecord

@admin.register(WorkShift)
class WorkShiftAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time', 'break_time')
    search_fields = ('name',)

@admin.register(AttendanceSheet)
class AttendanceSheetAdmin(admin.ModelAdmin):
    list_display = ('name', 'month', 'year', 'created_at')
    search_fields = ('name',)
    list_filter = ('month', 'year')
    filter_horizontal = ('positions',)

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('employee', 'sheet', 'date', 'status', 'check_in', 'check_out', 'working_hours')
    search_fields = ('employee__full_name', 'employee__code')
    list_filter = ('status', 'date')
    date_hierarchy = 'date'