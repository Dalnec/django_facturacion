from django.db import models
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager, models.Manager):
    def _create_user( self, username, password, is_staff, is_superuser, is_active, **extra_fields ):
        user = self.model(
            username=username,
            # email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
            **extra_fields
        )
        if is_superuser:
            user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        return self._create_user(
            username, password, True, True, True, **extra_fields
        )

    def create_user(self, username, password=None, **extra_fields):
        return self._create_user(
            username, password, False, False, True, **extra_fields
        )

    def cod_validation(self, id_user, codregistro):
        if self.filter(id=id_user, codregistro=codregistro).exists():
            return True
        else:
            return False

    def usuarios_sistema(self):
        return self.filter(is_superuser=False).order_by("-last_login")