from rest_framework import serializers
from .models import *

class DistricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distric
        fields = '__all__'


class SettingsSerializer(serializers.Serializer):
    interval_time_device = serializers.IntegerField(min_value=1)
    height = serializers.IntegerField(min_value=1)
    width = serializers.IntegerField(min_value=1)