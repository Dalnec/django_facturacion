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
        # ordering = ['-id']

    def __str__(self):
        return f"{self.id} - {self.usuario} - {self.measured}"
    
    @property
    def period(self):
        year = self.read_date.strftime('%Y')
        month = self.read_date.strftime('%m')
        if month == '01':
            month = 'Enero'
        elif month == '02':
            month = 'Febrero'
        elif month == '03':
            month = 'Marzo'
        elif month == '04':
            month = 'Abril'
        elif month == '05':
            month = 'Mayo'
        elif month == '06':
            month = 'Junio'
        elif month == '07':
            month = 'Julio'
        elif month == '08':
            month = 'Agosto'
        elif month == '09':
            month = 'Septiembre'
        elif month == '10':
            month = 'Octubre'
        elif month == '11':
            month = 'Noviembre'
        elif month == '12':
            month = 'Diciembre'
        return f"{month} {year}"

    def get_previous_measured(self):
        previous_invoice = Invoice.objects.filter(
            usuario=self.usuario,
            read_date__lt=self.read_date
        ).order_by('-read_date').first()
        return previous_invoice.measured if previous_invoice else 0

    def get_previous_month(self):
        previous_invoice = Invoice.objects.filter(
            usuario=self.usuario,
            read_date__lt=self.read_date
        ).order_by('-read_date').first()
        return previous_invoice.period if previous_invoice else '-'