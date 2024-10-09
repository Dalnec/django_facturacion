import datetime

from rest_framework import serializers
from .models import *

class MonitoringSerializer(serializers.ModelSerializer):
    isConnected = serializers.SerializerMethodField()

    class Meta:
        model = Monitoring
        fields = '__all__'

    def get_isConnected(self, obj):
        return obj.is_connected
    
    def create(self, validated_data):
        monitoring = Monitoring(**validated_data)
        monitoring.read_date = datetime.datetime.now()
        monitoring.save()
        return monitoring