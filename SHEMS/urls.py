"""
URL configuration for SHEMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from landing.views import landing_view, custom_login, logout_view, RegisterView
from accounts.views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", landing_view, name="Landing"),
    path("admin/", admin.site.urls),
    path("login/", custom_login, name="login"),
    path('logout/', logout_view, name='logout'),
    path("home/", customer_home_view, name="customer_home"),
    path("password-reset/", auth_views.PasswordResetView.as_view( template_name="registration/password_reset.html"), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view( template_name="registration/password_reset_sent.html"), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view( template_name="registration/password_reset_confirm.html"), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view( template_name="registration/password_reset_done.html"), name="password_reset_complete"),
    path('change_password/', change_password, name='change_password'),
    path("signup/",RegisterView.as_view(), name='signup'),
    path('service-locations/',service_locations, name='service_locations'),
    path('delete_location/<int:location_id>/', delete_location, name='delete_location'),
    path('manage_devices/', manage_devices, name='manage_devices'),
    path('devices/<int:location_id>/', devices_list, name='devices_list'),
    path('devices/delete/<int:device_id>/', delete_device, name='delete_device'), 
    path('devices/activate/<int:device_id>/', activate_device, name='activate_device'), 
    path('devices/pair_device/<int:location_id>/', pair_device, name='pair_device'),
    path('history-energy-usage/', history_energy_usage, name='history-energy-usage'),
    path('location-energy-usage/', location_energy_usage, name='location-energy-usage'),
    path('location-usage_history-comparison/', location_usage_history_comparison, name='location-usage-history-comparison'),
    path('peak-power/', peak_power_view, name='peak-power'),
    path('api/', include('accounts.api_urls')),
]

