import datetime

from rest_framework import serializers
from apps.distric.models import Distric
from .models import *

class MonitoringSerializer(serializers.ModelSerializer):
    isConnected = serializers.SerializerMethodField(read_only=True)
    interval_time_device = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Monitoring
        fields = '__all__'

    def get_isConnected(self, obj):
        if obj["percentage"]:
            return False
        return obj.is_connected

    def get_interval_time_device(self, obj):
        distric = Distric.objects.get(id=1)
        return distric.settings["interval_time_device"]
    
    def create(self, validated_data):
        monitoring = Monitoring(**validated_data)
        monitoring.read_date = datetime.datetime.now()
        monitoring.save()
        return monitoring