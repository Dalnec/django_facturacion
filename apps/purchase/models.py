from django.db import models
from model_utils.models import TimeStampedModel

class Purchase(TimeStampedModel):
    purchased_date = models.DateTimeField("Fecha de Compra", blank=True, null=True)
    total = models.DecimalField("Pago Total", max_digits=10, decimal_places=2, blank=True, null=True)
    liters = models.DecimalField("Cantidad Litros", max_digits=10, decimal_places=2, blank=True, null=True)
    active = models.BooleanField("Estado", default=True)
    price = models.DecimalField("Precio", max_digits=10, decimal_places=2, blank=True, null=True)
    observations = models.CharField('Observaciones', max_length=255, blank=True, null=True)
    employee = models.ForeignKey('user.Employee', related_name='fk_purchase_employee', on_delete=models.CASCADE)
    class Meta:
        db_table = 'Purchase'
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        # ordering = ['-id']

    def __str__(self):
        return f'{self.id} {self.total}'