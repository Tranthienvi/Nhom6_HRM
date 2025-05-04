from django.urls import path
from . import views

urlpatterns = [


	# Mẫu bảng lương
	path('mau-bang-luong/', views.payroll_template_list, name='payroll_template_list'),
	path('mau-bang-luong/them/', views.payroll_template_create, name='payroll_template_create'),
	path('mau-bang-luong/<int:pk>/', views.payroll_template_detail, name='payroll_template_detail'),
	path('mau-bang-luong/<int:pk>/cap-nhat/', views.payroll_template_update, name='payroll_template_update'),


	# Bảng lương
	path('bang-luong/', views.payroll_list, name='payroll_list'),
	path('bang-luong/them/', views.payroll_create, name='payroll_create'),
	path('bang-luong/<int:pk>/', views.payroll_detail, name='payroll_detail'),
	path('chi-tiet-luong/<int:pk>/cap-nhat/', views.payroll_detail_update, name='payroll_detail_update'),


	path('mau-bang-luong/<int:pk>/', views.payroll_template_detail, name='payroll_template_detail'),
]
