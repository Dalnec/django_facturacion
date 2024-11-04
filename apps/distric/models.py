from django.db import models
from model_utils.models import TimeStampedModel

class Distric(TimeStampedModel):
    name = models.CharField("Nombre", max_length=100)
    address = models.CharField("Dirección", max_length=100)
    representative = models.CharField("Representante", max_length=150)
    phone = models.CharField("Celular", max_length=100, blank=True, null=True)
    email = models.EmailField( "Correo", max_length=100, blank=True, null=True, unique=False )
    settings = models.JSONField("Configuraciones", blank=True, null=True)

    class Meta:
        ordering = ("id",)
        db_table = "Distric"
        verbose_name = "Barrio"
        verbose_name_plural = "Barrios"

    def __str__(self):
        return self.name
