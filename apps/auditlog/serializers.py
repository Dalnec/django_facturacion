from rest_framework import serializers
from .models import InvoiceHistory

class InvoiceHistorySerializer(serializers.ModelSerializer):
    employee_names = serializers.ReadOnlyField(source='employee.names')
    class Meta:
        model = InvoiceHistory
        fields = '__all__'