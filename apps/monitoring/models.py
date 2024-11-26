import datetime
from django.utils import timezone
from django.db import models
from model_utils.models import TimeStampedModel
from apps.distric.models import Distric
from decimal import Decimal

class Monitoring(TimeStampedModel):

    STATUS_CHOICES = (
        ('C', 'CONECTADO'),
        ('D', 'DESCONECTADO'),
    )
    
    read_date = models.DateTimeField("Fecha Lectura", blank=True, null=True)
    measured = models.DecimalField("Lectura Sensor", max_digits=18, decimal_places=2)
    percentage = models.CharField("Porcentaje", max_length=5)
    battery = models.CharField("Nivel Bateria", max_length=5)
    status = models.CharField("Estado", max_length=1, choices=STATUS_CHOICES, default='C')
    observations = models.CharField('Observaciones', max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Monitoring'
        # ordering = ['-id']

    def __str__(self):
        return f"{self.id} - {self.measured}"
    
    @property
    def is_connected(self):
        distric = Distric.objects.get(pk=1)
        interval = 10
        if distric.settings["interval_time_device"]:
            interval = distric.settings["interval_time_device"] / 60000
        now = datetime.datetime.now()
        read_date_naive = self.read_date.replace(tzinfo=None) if self.read_date.tzinfo else self.read_date
        # read_date_naive = self.read_date if not timezone.is_aware(self.read_date) else timezone.make_naive(self.read_date, datetime.timezone.utc)
        if read_date_naive >= now - datetime.timedelta(minutes=interval):
            return True
        return False
    
    @property
    def liters(self):
        distric = Distric.objects.get(pk=1)
        liters = None
        if self.measured and distric.settings["height"] and distric.settings["width"] and distric.settings["length"]:
            height = (Decimal(distric.settings["height"]) * Decimal(0.01)) - (Decimal(self.measured) * Decimal(0.01))
            width = Decimal(distric.settings["width"]) * Decimal(0.01)
            length = Decimal(distric.settings["length"]) * Decimal(0.01)
            liters = height * width * length
            liters = round(liters * 1000 , 2)
        return liters
    
    @property
    def height(self):
        distric = Distric.objects.get(pk=1)
        return distric.settings["height"] or 0
    
    @property
    def capacity(self):
        distric = Distric.objects.get(pk=1)
        liters = None
        if self.measured and distric.settings["height"] and distric.settings["width"] and distric.settings["length"]:
            height = Decimal(distric.settings["height"]) * Decimal(0.01)
            width = Decimal(distric.settings["width"]) * Decimal(0.01)
            length = Decimal(distric.settings["length"]) * Decimal(0.01)
            liters = height * width * length
            liters = round(liters * 1000 , 2)
        return liters