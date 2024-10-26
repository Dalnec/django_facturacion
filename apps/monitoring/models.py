import datetime
from django.utils import timezone
from django.db import models
from model_utils.models import TimeStampedModel

class Monitoring(TimeStampedModel):

    STATUS_CHOICES = (
        ('C', 'CONECTADO'),
        ('D', 'DESCONECTADO'),
    )
    
    read_date = models.DateTimeField("Fecha Lectura", blank=True, null=True)
    measured = models.DecimalField("Lectura Sensor", max_digits=18, decimal_places=2, blank=True, null=True)
    percentage = models.CharField("Porcentaje", max_length=5, blank=True, null=True)
    battery = models.CharField("Nivel Bateria", max_length=3, blank=True, null=True)
    status = models.CharField("Estado", max_length=1, choices=STATUS_CHOICES, default='C')
    observations = models.CharField('Observaciones', max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Monitoring'
        # ordering = ['-id']

    def __str__(self):
        return f"{self.id} - {self.measured}"
    
    @property
    def is_connected(self):
        now = datetime.datetime.now()
        read_date_naive = self.read_date.replace(tzinfo=None) if self.read_date.tzinfo else self.read_date
        # read_date_naive = self.read_date if not timezone.is_aware(self.read_date) else timezone.make_naive(self.read_date, datetime.timezone.utc)
        if read_date_naive >= now - datetime.timedelta(minutes=5):
            return True
        return False
