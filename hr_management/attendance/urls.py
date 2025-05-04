from django.urls import path
from . import views

urlpatterns = [
    path('', views.attendance_dashboard, name='attendance_dashboard'),
    path('ca-lam-viec/', views.work_shift_list, name='work_shift_list'),
    path('ca-lam-viec/them/', views.work_shift_create, name='work_shift_create'),
    path('bang-cham-cong/', views.attendance_sheet_list, name='attendance_sheet_list'),
    path('bang-cham-cong/them/', views.attendance_sheet_create, name='attendance_sheet_create'),
    path('bang-cham-cong/<int:pk>/', views.attendance_sheet_detail, name='attendance_sheet_detail'),
    path('bang-cham-cong/<int:sheet_id>/nhan-vien/<int:employee_id>/them-ban-ghi/',
         views.attendance_record_create, name='attendance_record_create'),
]
