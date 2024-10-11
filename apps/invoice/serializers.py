from rest_framework import serializers
from .models import *

class InvoiceSerializer(serializers.ModelSerializer):
    period = serializers.SerializerMethodField()
    class Meta:
        model = Invoice
        fields = '__all__'
    
    def get_period(self, obj):
        return obj.period