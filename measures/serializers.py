from rest_framework import serializers
from  .models import *
from datetime import datetime, timedelta

class MeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measure
        fields = ['value', 'created_at']

class DeviceMeasureSerializer(serializers.ModelSerializer):
    # measure = MeasureSerializer()
    value = serializers.ReadOnlyField(source='measure.value')
    created_at = serializers.ReadOnlyField(source='measure.created_at')

    class Meta:
        model = DeviceMeasure
        fields = ['value', 'created_at']

class DeviceSerializer(serializers.ModelSerializer):
    measures = DeviceMeasureSerializer(many=True, read_only=True)
    class Meta:
        model = Device
        fields = ['title', 'longitude', 'latitude', 'measures']

class RemoteAddressesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceRemoteAddr
        fields = ['latest_ip', 'created_at']

class UserDeviceSerializer(serializers.ModelSerializer):
    measures = DeviceMeasureSerializer(many=True, read_only=True)
    remote_addresses = RemoteAddressesSerializer(many=True, read_only=True)
    class Meta:
        model = Device
        fields = ['title', 'longitude', 'latitude', 'measures', 'remote_addresses']