from rest_framework import viewsets, permissions
from .models import *
from .serializers import DeviceSerializer, UserDeviceSerializer
from rest_framework.mixins import UpdateModelMixin
from .throttles import BurstRateThrottle, SustainedRateThrottle, DeviceThrottle
from rest_framework.throttling import AnonRateThrottle
from django.db.models import Prefetch
from datetime import datetime, timedelta

class HourlyUserDeviceViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']    
    throttle_classes = (BurstRateThrottle,SustainedRateThrottle)
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserDeviceSerializer
    def get_queryset(self):
        time_treshold = datetime.now() - timedelta(days=1)
        return Device.objects.filter(user=self.request.user).prefetch_related(Prefetch('measures', queryset=DeviceMeasure.objects.filter(measure__created_at__gte=time_treshold))).prefetch_related(Prefetch('remote_addresses', queryset=DeviceRemoteAddr.objects.filter(created_at__gte=time_treshold)))


class DailyUserDeviceViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']    
    throttle_classes = (BurstRateThrottle,SustainedRateThrottle)
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserDeviceSerializer
    def get_queryset(self):
        time_treshold = datetime.now() - timedelta(days=7)
        return Device.objects.filter(user=self.request.user).prefetch_related(Prefetch('measures', queryset=DeviceMeasure.objects.filter(measure__created_at__gte=time_treshold))).prefetch_related(Prefetch('remote_addresses', queryset=DeviceRemoteAddr.objects.filter(created_at__gte=time_treshold)))
      
class HourlyPublicDeviceViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    throttle_classes = (BurstRateThrottle,SustainedRateThrottle)
    
    serializer_class = DeviceSerializer
    def get_queryset(self):
        time_treshold = datetime.now() - timedelta(days=1)
        return Device.objects.filter(is_visible=True).prefetch_related(Prefetch('measures', queryset=DeviceMeasure.objects.filter(measure__created_at__gte=time_treshold)))

class DailyPublicDeviceViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    throttle_classes = (BurstRateThrottle,SustainedRateThrottle)
    
    serializer_class = DeviceSerializer
    def get_queryset(self):
        time_treshold = datetime.now() - timedelta(days=7)
        return Device.objects.filter(is_visible=True).prefetch_related(Prefetch('measures', queryset=DeviceMeasure.objects.filter(measure__created_at__gte=time_treshold)))
