from rest_framework import routers
from measures.views import HourlyUserDeviceViewSet, DailyUserDeviceViewSet, HourlyPublicDeviceViewSet, DailyPublicDeviceViewSet

router = routers.DefaultRouter()
router.register('user_device_hourly', HourlyUserDeviceViewSet, basename='user_device_hourly')
router.register('user_device_daily', DailyUserDeviceViewSet, basename='user_device_daily')
router.register('public_device_hourly', HourlyPublicDeviceViewSet, basename='public_device_hourly')
router.register('public_device_daily', DailyPublicDeviceViewSet, basename='public_device_daily')

