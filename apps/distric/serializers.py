from rest_framework import serializers
from .models import *

class DistricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distric
        fields = '__all__'


class SettingsSerializer(serializers.Serializer):
    interval_time_device = serializers.IntegerField(min_value=1)
    height = serializers.CharField()
    width = serializers.CharField()
    length = serializers.CharField()

    def to_representation(self, instance):
        """
        Convierte los valores del modelo al formato deseado para la respuesta.
        """
        representation = super().to_representation(instance)
        # Convertir milisegundos a minutos
        if 'interval_time_device' in representation:
            representation['interval_time_device'] = representation['interval_time_device'] / 60000  # Milisegundos a minutos
        return representation

    def to_internal_value(self, data):
        """
        Convierte los datos de entrada al formato interno esperado por el modelo.
        """
        # Convertir minutos a milisegundos
        if 'interval_time_device' in data:
            try:
                data['interval_time_device'] = int(float(data['interval_time_device']) * 60000)  # Minutos a milisegundos
            except ValueError:
                raise serializers.ValidationError({
                    'interval_time_device': 'Debe ser un número válido.'
                })
        return super().to_internal_value(data)