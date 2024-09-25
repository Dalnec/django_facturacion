from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from model_utils.models import TimeStampedModel
from .manager import UserManager


class Profile(TimeStampedModel):
    description = models.CharField('Descripcion', max_length=75)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'Profile'
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles'
        ordering = ['id']

    def __str__(self):
        return f'{self.id} {self.description}'



class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Usuario', max_length=20, unique=True)
    profile = models.ForeignKey(Profile, related_name='fk_user_profile', on_delete=models.SET_NULL, null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_owner = models.BooleanField(default=False)

    USERNAME_FIELD = "username"

    objects = UserManager()

    def save(self, **kwargs):
        self.username = self.username.upper()
        super(User, self).save()

    class Meta:
        db_table = "User"
        verbose_name_plural = "Usuarios Sistema"
        ordering = ["-id"]

    def __str__(self):
        if self.profile:
            return f"{self.username} -- {self.profile.description}"
        return f"{self.username} -- Sin perfil"

        
class Employee(TimeStampedModel):
    STATUS_CHOICES = [
        ("A", "ACTIVO"),
        ("I", "INACTIVO"),
    ]
    
    ci = models.CharField('Carnet de Identidad', unique=True, max_length=8, blank=True, null=True)
    names = models.CharField('Nombres', max_length=150, blank=True)
    lastnames = models.CharField('Apellidos', max_length=150, blank=True)
    email = models.EmailField('Correo', max_length=150, blank=True, null=True)
    phone = models.CharField('Telefono', max_length=15, blank=True, null=True)
    address = models.CharField('Direccion', max_length=150, blank=True, null=True)
    status = models.CharField("Estado", max_length=1, choices=STATUS_CHOICES, default='A')
    user = models.OneToOneField(User, on_delete=models.SET_NULL, related_name="fk_employee_user", null=True, blank=True)

    def save(self, **kwargs):
        self.names = self.names.upper()
        self.lastnames = self.lastnames.upper()
        super(Employee, self).save()

    class Meta:
        db_table = "Employee"
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
        ordering = ["-id"]

    def __str__(self):
        return f"{self.ci} -- {self.names} -- {self.lastnames}"
    
    @property
    def fullname(self):
        return f"{self.names} {self.lastnames}"