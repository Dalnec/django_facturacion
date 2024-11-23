from rest_framework import serializers
from .models import *

class UsuarioSerializer(serializers.ModelSerializer):
    hasDebt = serializers.SerializerMethodField(read_only=True)
    makeInvoice = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Usuario
        fields = '__all__'
    
    def get_hasDebt(self, obj):
        return obj.hasDebt

    def get_makeInvoice(self, obj):
        return obj.makeInvoice


class UsuarioDetailSerializer(serializers.ModelSerializer):
    invoice_number = serializers.ReadOnlyField()
    invoice_status = serializers.ReadOnlyField()

    class Meta:
        model = UsuarioDetail
        fields = '__all__'


class UsuarioDetailTicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = UsuarioDetail
        fields = [ "description", "price", "quantity", "subtotal", "is_income" ]