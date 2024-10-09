import datetime

from django.db import models
from model_utils.models import TimeStampedModel

class Monitoring(TimeStampedModel):

    STATUS_CHOICES = (
        ('C', 'CONECTADO'),
        ('D', 'DESCONECTADO'),
    )
    
    read_date = models.DateTimeField("Fecha Lectura", blank=True, null=True)
    measured = models.DecimalField("Lectura Medidor", max_digits=18, decimal_places=2, blank=True, null=True)
    status = models.CharField("Estado", max_length=1, choices=STATUS_CHOICES, default='C')
    observations = models.CharField('Observaciones', max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Monitoring'
        ordering = ['-id']

    def __str__(self):
        return f"{self.id} - {self.measured}"
    
    @property
    def is_connected(self):
        if self.read_date >= datetime.datetime.now() - datetime.timedelta(minutes=5):
            return True
        return False
