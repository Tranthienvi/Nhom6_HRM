from django.urls import path
from . import views

urlpatterns = [
    # Employee URLs
    path('', views.employee_list, name='employee_list'),
    path('<int:pk>/', views.employee_detail, name='employee_detail'),
    path('them/', views.employee_create, name='employee_create'),
    path('<int:pk>/cap-nhat/', views.employee_update, name='employee_update'),

    # Contract URLs
    path('<int:employee_id>/hop-dong/them/', views.contract_create, name='contract_create'),
]
