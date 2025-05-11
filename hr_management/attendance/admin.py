from django.contrib import admin
from .models import AttendanceRecord, AttendanceSheet, DailyAttendance, WorkShift

@admin.register(WorkShift)
class WorkShiftAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'start_time', 'end_time')
    search_fields = ('name', 'code')


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('employee', 'attendance_date', 'status', 'check_in', 'check_out', 'work_hours', 'overtime')
    list_filter = ('status', 'attendance_date')
    search_fields = ('employee__full_name',)  # Sử dụng trường 'full_name' từ model Employee


@admin.register(AttendanceSheet)
class AttendanceSheetAdmin(admin.ModelAdmin):
    list_display = ('name', 'month', 'year', 'status', 'created_at')
    list_filter = ('status', 'month', 'year')
    search_fields = ('name',)


@admin.register(DailyAttendance)
class DailyAttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'attendance_record', 'attendance_status', 'work_shift')
    list_filter = ('attendance_status', 'date')
    search_fields = ('employee__full_name', 'attendance_record__name')