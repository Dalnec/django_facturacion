from rest_framework import serializers
from .models import InvoiceHistory

class InvoiceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceHistory
        fields = '__all__'