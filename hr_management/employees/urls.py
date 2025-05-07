from django.urls import path
from . import views

# urlpatterns = [
#     path('create/', views.employee_create, name='employee_create'),
#     path('', views.employee_list, name='employee_list'),
#     path('<int:pk>/', views.employee_detail, name='employee_detail'),
#     path('them/', views.employee_create, name='employee_create'),
#     path('<int:pk>/cap-nhat/', views.employee_update, name='employee_update'),
#     path('<int:employee_id>/hop-dong/them/', views.contract_create, name='contract_create'),  # Thêm URL cho việc tạo hợp đồng
# ]


urlpatterns = [
    # Employee URLs
    path('', views.employee_list, name='employee_list'),
    path('them/', views.employee_create, name='employee_create'),
    path('<int:pk>/', views.employee_detail, name='employee_detail'),
    path('<int:pk>/cap-nhat/', views.employee_update, name='employee_update'),

    # Contract URLs
    path('hop-dong/', views.contract_list, name='contract_list'),
    path('hop-dong/them/', views.contract_create, name='contract_create_general'),
    path('hop-dong/<int:pk>/', views.contract_detail, name='contract_detail'),
    path('hop-dong/<int:pk>/cap-nhat/', views.contract_update, name='contract_update'),
    path('hop-dong/<int:pk>/cham-dut/', views.contract_terminate, name='contract_terminate'),
    path('<int:employee_id>/hop-dong/them/', views.contract_create, name='contract_create'),
    path('contracts/create/', views.contract_create_general, name='contract_create_general'),


    # Personnel URLs
    path('tong-quan/', views.personnel_overview, name='personnel_overview'),
    path('ho-so/', views.personnel_profile, name='personnel_profile'),
]