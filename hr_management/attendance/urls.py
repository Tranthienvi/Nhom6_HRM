from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='attendance_dashboard'),
    path('work-shifts/', views.work_shift_list, name='work_shift_list'),
    path('work-shifts/add/', views.work_shift_form, name='work_shift_form'),
    path('work-shifts/edit/<int:id>/', views.work_shift_form, name='work_shift_form'),
    path('work-shifts/detail/<int:id>/', views.work_shift_detail, name='work_shift_detail'),
    path('work-shifts/delete/<int:id>/', views.work_shift_delete, name='work_shift_delete'),
    path('attendance-details/', views.attendance_detail_list, name='attendance_detail_list'),
    path('attendance-details/add/', views.attendance_detail_form, name='attendance_detail_form'),
    path('attendance-details/edit/<int:id>/', views.attendance_detail_form, name='attendance_detail_form'),
    path('attendance-details/delete/<int:id>/', views.attendance_detail_delete, name='attendance_detail_delete'),
    path('attendance-details/view/<int:id>/', views.attendance_detail_view, name='attendance_detail_view'),
    path('attendance-details/update/<int:record_id>/<int:employee_id>/<str:date_str>/', views.update_daily_attendance, name='update_daily_attendance'),
    path('attendance-details/get/<int:record_id>/<int:employee_id>/<str:date_str>/', views.get_daily_attendance, name='get_daily_attendance'),
    path('attendance-summary/', views.attendance_summary, name='attendance_summary'),
    path('attendance-summary/add/', views.attendance_summary_form, name='attendance_summary_form'),
    path('attendance-summary/edit/<int:id>/', views.attendance_summary_form, name='attendance_summary_form'),
    path('attendance-summary/view/<int:id>/', views.attendance_summary_view, name='attendance_summary_view'),
    path('attendance-summary/delete/<int:id>/', views.attendance_summary_delete, name='attendance_summary_delete'),
    path('attendance-summary/transfer-to-payroll/<int:id>/', views.transfer_to_payroll, name='transfer_to_payroll'),
    path('attendance-summary/send-confirmation/<int:id>/', views.send_confirmation, name='send_confirmation'),
]