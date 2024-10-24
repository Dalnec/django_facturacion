from rest_framework import serializers
from .models import *

class PurchaseSerializer(serializers.ModelSerializer):
    employee_name = serializers.ReadOnlyField(source="employee.names")
    class Meta:
        model = Purchase
        fields = '__all__'