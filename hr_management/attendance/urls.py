from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.attendance_dashboard, name='attendance_dashboard'),
    path('dashboard/', views.payroll_dashboard, name='payroll_dashboard'),

    # Bảng chấm công
    path('bang-cham-cong/', views.attendance_sheet_list, name='attendance_sheet_list'),
    path('bang-cham-cong/them/', views.attendance_sheet_create, name='attendance_sheet_create'),
    path('bang-cham-cong/<int:pk>/', views.attendance_sheet_detail, name='attendance_sheet_detail'),
    path('bang-cham-cong/<int:pk>/sua/', views.attendance_sheet_update, name='attendance_sheet_update'),
    path('bang-cham-cong/<int:pk>/xuat-csv/', views.export_attendance_sheet, name='export_attendance_sheet'),

    # Bản ghi chấm công
    path('du-lieu-cham-cong/them/', views.attendance_record_create, name='attendance_record_create'),
    path('bang-cham-cong/<int:sheet_id>/du-lieu/them/', views.attendance_record_create,
         name='attendance_record_create_for_sheet'),
    path('bang-cham-cong/<int:sheet_id>/nhan-vien/<int:employee_id>/du-lieu/them/', views.attendance_record_create,
         name='attendance_record_create_for_employee'),
    path('du-lieu-cham-cong/<int:pk>/sua/', views.attendance_record_update, name='attendance_record_update'),
    path('du-lieu-cham-cong/<int:pk>/xoa/', views.attendance_record_delete, name='attendance_record_delete'),

    # Ca làm việc
    path('ca-lam-viec/', views.work_shift_list, name='work_shift_list'),
    path('ca-lam-viec/them/', views.work_shift_create, name='work_shift_create'),
    path('ca-lam-viec/<int:pk>/sua/', views.work_shift_update, name='work_shift_update'),

    # Chuyển dữ liệu tính lương
    path('bang-cham-cong/<int:sheet_id>/chuyen-tinh-luong/', views.transfer_attendance_data,
         name='transfer_attendance_data'),

    # Bảng lương
    path('bang-luong/', views.payroll_list, name='payroll_list'),
    path('bang-luong/them/', views.payroll_create, name='payroll_create'),
    path('bang-luong/<int:pk>/', views.payroll_detail, name='payroll_detail'),

    # Mẫu bảng lương
    path('mau-bang-luong/', views.payroll_template_list, name='payroll_template_list'),
    path('mau-bang-luong/them/', views.payroll_template_create, name='payroll_template_create'),
    path('mau-bang-luong/<int:pk>/', views.payroll_template_detail, name='payroll_template_detail'),
    path('mau-bang-luong/<int:template_id>/thanh-phan/them/', views.payroll_component_create,
         name='payroll_component_create'),
]
