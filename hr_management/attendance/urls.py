from django.urls import path
from . import views

urlpatterns = [
    path('', views.payroll_dashboard, name='payroll_dashboard'),
    path('mau-bang-luong/', views.payroll_template_list, name='payroll_template_list'),
    path('mau-bang-luong/them/', views.payroll_template_create, name='payroll_template_create'),
    path('mau-bang-luong/<int:pk>/', views.payroll_template_detail, name='payroll_template_detail'),
    path('mau-bang-luong/<int:template_id>/thanh-phan/them/', views.payroll_component_create, name='payroll_component_create'),
    path('bang-luong/', views.payroll_list, name='payroll_list'),
    path('bang-luong/them/', views.payroll_create, name='payroll_create'),
    path('bang-luong/<int:pk>/', views.payroll_detail, name='payroll_detail'),

    path('dashboard/', views.attendance_dashboard, name='attendance_dashboard'),
    path('shifts/', views.work_shift_list, name='work_shift_list'),
    path('sheets/', views.attendance_sheet_list, name='attendance_sheet_list'),
    path('attendance/create/', views.attendance_sheet_create, name='attendance_sheet_create'),
    path('work-shift/create/', views.work_shift_create, name='work_shift_create'),

    path('mau-bang-luong/<int:template_id>/thanh-phan/them/', views.payroll_component_create, name='payroll_component_create'),
    path('mau-bang-luong/<int:pk>/', views.payroll_template_detail, name='payroll_template_detail'),
    # URL mới cho chức năng chuyển tính lương
    path('bang-cham-cong/<int:sheet_id>/chuyen-tinh-luong/', views.transfer_attendance_data, name='transfer_attendance_data'),
]
