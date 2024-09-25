from rest_framework import serializers
from .models import *

class DistricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distric
        fields = '__all__'