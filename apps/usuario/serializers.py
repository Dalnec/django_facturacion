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