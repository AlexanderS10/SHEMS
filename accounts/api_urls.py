from django.urls import path
from .views import EnergyUsageDataDevice24, EnergyUsageDataLocation24
urlpatterns = [
        path('energy-usage-device-24/', EnergyUsageDataDevice24.as_view(), name='energy-usage-device-api'),
        path('energy-usage-location-24/', EnergyUsageDataLocation24.as_view(), name='energy-usage-device-api'),
]