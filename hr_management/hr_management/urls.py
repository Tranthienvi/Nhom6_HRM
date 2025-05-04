from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home, login_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('nhan-vien/', include('employees.urls')),
    path('cham-cong/', include('attendance.urls')),
    path('tien-luong/', include('payroll.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)