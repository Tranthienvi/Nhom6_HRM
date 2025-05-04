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
]
