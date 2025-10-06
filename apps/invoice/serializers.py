import json
from decimal import Decimal
from rest_framework import serializers
from .models import Invoice
from apps.usuario.serializers import UsuarioDetailTicketSerializer

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
        return obj.usuario.code or ""
    
    def get_full_name(self, obj):
        return obj.usuario.full_name

class TicketBodySerializer(serializers.ModelSerializer):
    previous_reading = serializers.SerializerMethodField(read_only=True)
    actual_reading = serializers.CharField(source='measured', read_only=True)
    previous_month = serializers.SerializerMethodField(read_only=True)
    actual_month = serializers.SerializerMethodField(source='measured', read_only=True)
    consumed = serializers.SerializerMethodField(read_only=True)
    total = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Invoice
        fields = ('previous_reading', 'actual_reading', 'price', 'total', 'subtotal',
            'previous_month', 'actual_month', 'consumed')

    def get_previous_month(self, obj):
        return obj.get_previous_month()

    def get_actual_month(self, obj):
        return obj.period

    def get_previous_reading(self, obj):
        return str(obj.get_previous_measured())

    def get_consumed(self, obj):
        return str(obj.measured - Decimal(self.get_previous_reading(obj)))
    
    def get_total(self, obj):
        # usuario_detail = obj.fk_usuariodetail_invoice.filter(status=True)
        # details = UsuarioDetailTicketSerializer(usuario_detail, many=True).data
        # if details:
        #     return str(Decimal(obj.total) + sum(Decimal(detail['subtotal']) for detail in details))
        # obj.calculate_total()
        return str(obj.total)

class InvoiceSerializer(serializers.ModelSerializer):
    period = serializers.SerializerMethodField()
    ticket = serializers.SerializerMethodField()
    employeeName = serializers.SerializerMethodField()
    previosMeasured = serializers.SerializerMethodField()
    measured_diff = serializers.ReadOnlyField()

    class Meta:
        model = Invoice
        fields = '__all__'
    
    def get_period(self, obj):
        return obj.period

    def get_ticket(self, obj):
        header = TicketHeaderSerializer(obj).data
        body = TicketBodySerializer(obj).data
        usuario_detail = obj.fk_usuariodetail_invoice.filter(invoice__isnull=False, status=True)
        details = UsuarioDetailTicketSerializer(usuario_detail, many=True).data
        # return {
        #     'header': header,
        #     'body': body,
        #     'details': details,
        # }
        return json.dumps({
            'header': header,
            'body': body,
            'details': details,
        })

    def get_employeeName(self, obj):
        return obj.employee.names
    
    def get_previosMeasured(self, obj):
        return f"{obj.get_previous_measured()}"