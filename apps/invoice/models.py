import locale
from django.db import models
from model_utils.models import TimeStampedModel

class Invoice(TimeStampedModel):

    STATUS_CHOICES = (
        ('D', 'DEUDA'),
        ('P', 'PAGADO'),
    )
    
    employee = models.ForeignKey('user.Employee', related_name='fk_invoice_employee', on_delete=models.CASCADE)
    usuario = models.ForeignKey('usuario.Usuario', related_name='fk_invoice_usuario', on_delete=models.CASCADE)
    read_date = models.DateTimeField("Fecha Lectura", blank=True, null=True)
    measured = models.DecimalField("Lectura Medidor", max_digits=18, decimal_places=2, blank=True, null=True)
    price = models.DecimalField("Precio", max_digits=18, decimal_places=2, blank=True, null=True)
    total = models.DecimalField("Total", max_digits=18, decimal_places=2, blank=True, null=True)
    status = models.CharField("Estado", max_length=1, choices=STATUS_CHOICES, default='D')
    observations = models.CharField('Observaciones', max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Invoice'
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        ordering = ['-id']

    def __str__(self):
        return f"{self.id} - {self.usuario} - {self.measured}"
    
    @property
    def period(self):
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        return self.read_date.strftime('%B %Y')