from django.urls import path
from .views import EnergyUsageDataDevice24, EnergyUsageDataLocation24,HistoryEnergyUsageAPIView, DeviceEnergyUsageAPIView
urlpatterns = [
        path('energy-usage-device-24/', EnergyUsageDataDevice24.as_view(), name='energy-usage-device-api'),
        path('energy-usage-location-24/', EnergyUsageDataLocation24.as_view(), name='energy-usage-device-api'),
        path('history-energy-usage/<int:location_id>/', HistoryEnergyUsageAPIView.as_view(), name='history-energy-usage-api'),
        path('device-energy-usage-date/', DeviceEnergyUsageAPIView.as_view(), name='device-energy-usage-date-api'),
]