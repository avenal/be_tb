from rest_framework.throttling import UserRateThrottle
from rest_framework.throttling import AnonRateThrottle

class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'

class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'

class DeviceThrottle(AnonRateThrottle):
    scope = 'device'