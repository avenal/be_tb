from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model

# Create your models here.
class Measure(models.Model):
    created_at = models.DateTimeField()
    value = models.IntegerField()

class Device(models.Model):
    title = models.CharField(max_length=127, null=True, blank=True)
    client_id = models.CharField(max_length=127, primary_key=True)    
    mac_address = models.CharField(max_length=63, blank=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    is_visible = models.BooleanField(default=False)
    user = models.ForeignKey(get_user_model(), related_name='devices', on_delete=models.DO_NOTHING, null=True)

class DeviceRemoteAddr(models.Model):
    created_at = models.DateTimeField()
    latest_ip = models.CharField(max_length=63)
    device = models.ForeignKey(Device, related_name='remote_addresses', on_delete=models.DO_NOTHING)

class DeviceMeasure(models.Model):
    device = models.ForeignKey(Device, related_name='measures', on_delete=models.DO_NOTHING)
    measure = models.ForeignKey(Measure, on_delete=models.DO_NOTHING)

class Aggregation(models.Model):
    created_at = models.DateTimeField(default=datetime.now)
    status = models.CharField(max_length=15)

class Log(models.Model):
    payload = models.TextField(max_length=32767)
    processed = models.TextField(max_length=32767)

class AggregationLog(models.Model):
    aggregation = models.ForeignKey(Aggregation, on_delete=models.DO_NOTHING)
    log = models.ForeignKey(Log, on_delete=models.DO_NOTHING)
