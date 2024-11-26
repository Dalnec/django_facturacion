import datetime

from rest_framework import serializers
from apps.distric.models import Distric
from .models import *

class MonitoringSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monitoring
        fields = '__all__'

    def create(self, validated_data):
        monitoring = Monitoring(**validated_data)
        monitoring.read_date = datetime.datetime.now()
        monitoring.save()
        return monitoring

class LastMonitoringSerializer(serializers.ModelSerializer):
    isConnected = serializers.SerializerMethodField(read_only=True)
    interval_time_device = serializers.SerializerMethodField(read_only=True)
    liters = serializers.ReadOnlyField()
    height = serializers.ReadOnlyField()
    capacity = serializers.ReadOnlyField()
    class Meta:
        model = Monitoring
        fields = '__all__'

    def get_isConnected(self, obj):
        return obj.is_connected

    def get_interval_time_device(self, obj):
        distric = Distric.objects.get(id=1)
        return distric.settings["interval_time_device"]
