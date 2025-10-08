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
    code = models.CharField("Codigo Medidor", max_length=10, blank=True, null=True)
    last_measured = models.DecimalField("Ultima Lectura Medidor", max_digits=18, decimal_places=2, blank=True, null=True)
    restart = models.BooleanField("Reinicio", default=False)

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
        # # validar que la factura solo se realice una vez por mes y sea consecutivo
        # # TODO: validar 20 dias por configuracion
        last_invoice = invoices.order_by('-read_date').first()
        now = timezone.now()
        twenty_days_ago = now - datetime.timedelta(days=20)
        # if last_invoice.read_date.month != now.month and last_invoice.read_date <= twenty_days_ago:
        #     return True
        # else:
        #     return False
        
        # Validar que sea un mes y año distinto al actual
        is_different_month = last_invoice.read_date.month != now.month
        is_different_year = last_invoice.read_date.year != now.year

        if (is_different_month or is_different_year) and last_invoice.read_date <= twenty_days_ago:
            return True
        else:
            return False
    
    @property
    def status_description(self):
        return dict(self.STATUS_CHOICES)[self.status]
    
    @property
    def lastInvoice(self):
        invoice = self.fk_invoice_usuario.order_by('-read_date').first()
        if not invoice:
            return None
        return f"{invoice.period} -> {invoice.measured}"
    
    def generate_code(self):
        # caracter "M" y llenado con dos ceros seguido con el id
        return f"M{str(self.id).zfill(4)}"


class UsuarioDetail(TimeStampedModel):

    usuario = models.ForeignKey( "usuario.Usuario", on_delete=models.SET_NULL, related_name="fk_usuariodetail_usuario", null=True, blank=True ) 
    invoice = models.ForeignKey( "invoice.Invoice", on_delete=models.SET_NULL, related_name="fk_usuariodetail_invoice", null=True, blank=True )
    description = models.CharField("Descripcion", max_length=255, blank=True, null=True)
    price = models.DecimalField("Precio", max_digits=18, decimal_places=2, blank=True, null=True)
    quantity = models.DecimalField("Cantidad", max_digits=18, decimal_places=2, blank=True, null=True)
    subtotal = models.DecimalField("Subtotal", max_digits=18, decimal_places=2, blank=True, null=True)
    is_income = models.BooleanField("Es Ingreso?", default=True)
    status = models.BooleanField("Estado", default=True)
    
    class Meta:
        ordering = ("-id",)
        db_table = "UsuarioDetail"
        verbose_name = "UsuarioDetail"
    
    def __str__(self):
        return f"{self.id} - {self.usuario} - {self.description} - {self.status}"
    
    @property
    def invoice_number(self):
        return self.invoice.id if self.invoice else None
    
    @property
    def invoice_status(self):
        return dict(self.invoice.STATUS_CHOICES)[self.invoice.status] if self.invoice else None

    @classmethod
    def generate_mora(cls, usuario, amount, invoice=None):
         cls.objects.create(
            usuario = usuario,
            description = 'Cobro de Mora',
            price = amount,
            quantity = 1,
            subtotal = amount,
            invoice = invoice
        )