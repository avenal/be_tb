from django.contrib import admin
from .models import *

admin.site.register(Measure)
admin.site.register(Device)
admin.site.register(DeviceMeasure)
admin.site.register(Aggregation)
admin.site.register(Log)
admin.site.register(DeviceRemoteAddr)
admin.site.register(AggregationLog)
