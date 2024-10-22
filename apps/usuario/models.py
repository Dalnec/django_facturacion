import datetime
from django.utils import timezone
from django.db import models
from model_utils.models import TimeStampedModel

class Usuario(TimeStampedModel):

    GENDER_CHOICES = [
        ("F", "FEMENINO"),
        ("M", "MASCULINO"),
    ]

    STATUS_CHOICES = [
        ("A", "ACTIVO"),
        ("I", "INACTIVO"),
    ]

    ci = models.CharField( "Número CI", max_length=10, unique=True)
    names = models.CharField("Nombres", max_length=150)
    lastnames = models.CharField("Apellidos", max_length=150)
    gender = models.CharField( "Género", max_length=1, choices=GENDER_CHOICES, blank=True, null=True )
    phone = models.CharField("Celular", max_length=11, blank=True, null=True)
    email = models.EmailField('Correo', max_length=150, blank=True, null=True)
    family = models.CharField("Nombre Familia", max_length=255, blank=True, null=True)
    address = models.CharField("Direccion", max_length=255, blank=True, null=True)
    status = models.CharField("Estado", max_length=1, choices=STATUS_CHOICES, default='A')
    user = models.OneToOneField( "user.User", on_delete=models.SET_NULL, related_name="fk_usuario_user", null=True, blank=True ) 
    employee = models.ForeignKey( "user.Employee", on_delete=models.SET_NULL, related_name="fk_usuario_employee", null=True, blank=True) 

    class Meta:
        ordering = ("-id",)
        db_table = "Usuario"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f"{str(self.id)} - {self.names}"
    
    @property
    def full_name(self):
        return f"{self.names} {self.lastnames}"
    
    @property
    def hasDebt(self):
        return self.fk_invoice_usuario.filter(status='D').exists()

    @property
    def makeInvoice(self):
        invoices = self.fk_invoice_usuario
        if not invoices.exists():
            return True
        last_invoice = invoices.first()
        # validar que la factura solo se realice una vez por mes y sea consecutivo
        now = timezone.now()
        # TODO: validar 20 dias por configuracion
        if last_invoice.read_date.month != now.month and last_invoice.read_date <= now - datetime.timedelta(days=20):
            return True
        else:
            return False