from rest_framework import serializers
from .models import *

class MonitoringSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monitoring
        fields = '__all__'