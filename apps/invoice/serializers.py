import json
from rest_framework import serializers
from .models import *
from decimal import Decimal

class TicketHeaderSerializer(serializers.ModelSerializer):
    emission_date = serializers.SerializerMethodField(read_only=True)
    medidor = serializers.SerializerMethodField(read_only=True)
    full_name = serializers.SerializerMethodField(read_only=True)
    address = serializers.CharField(source='usuario.address', read_only=True)
    number = serializers.CharField(source='id', read_only=True)

    class Meta:
        model = Invoice
        fields = ('number', 'emission_date', 'medidor', 'full_name', 'address')

    def get_emission_date(self, obj):
        return obj.read_date.strftime('%d/%m/%Y')
    
    def get_medidor(self, obj):
        return 'E365498'
    
    def get_full_name(self, obj):
        return obj.usuario.full_name

class TicketBodySerializer(serializers.ModelSerializer):
    previous_reading = serializers.SerializerMethodField(read_only=True)
    actual_reading = serializers.CharField(source='measured', read_only=True)
    previous_month = serializers.SerializerMethodField(read_only=True)
    actual_month = serializers.SerializerMethodField(source='measured', read_only=True)
    consumed = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Invoice
        fields = ('previous_reading', 'actual_reading', 'price', 'total', 
            'previous_month', 'actual_month', 'consumed')

    def get_previous_month(self, obj):
        return obj.get_previous_month()

    def get_actual_month(self, obj):
        return obj.period

    def get_previous_reading(self, obj):
        return str(obj.get_previous_measured())

    def get_consumed(self, obj):
        return str(obj.measured - Decimal(self.get_previous_reading(obj)))

class InvoiceSerializer(serializers.ModelSerializer):
    period = serializers.SerializerMethodField()
    ticket = serializers.SerializerMethodField()
    employeeName = serializers.SerializerMethodField()
    previosMeasured = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = '__all__'
    
    def get_period(self, obj):
        return obj.period

    def get_ticket(self, obj):
        header = TicketHeaderSerializer(obj).data
        body = TicketBodySerializer(obj).data
        # return {
        #     'header': header,
        #     'body': body
        # }
        return json.dumps({
            'header': header,
            'body': body
        })

    def get_employeeName(self, obj):
        return obj.employee.names
    
    def get_previosMeasured(self, obj):
        return obj.get_previous_measured()