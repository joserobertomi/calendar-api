from django.db import models
from ..validators import *
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from localflavor.br.models import BRCPFField

class UserManager(BaseUserManager):
    def create_user(self, cpf, password=None, **extra_fields):
        if not cpf:
            raise ValueError('O usuário deve ter um CPF')
        user = self.model(cpf=cpf, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        if not extra_fields.get('is_superuser', False):
            try:
                default_group = Group.objects.get(name='DefaultUser')
                user.groups.add(default_group)
            except Group.DoesNotExist:
                pass
            
        return user

    def create_superuser(self, cpf, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('O superusuário deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('O superusuário deve ter is_superuser=True.')

        return self.create_user(cpf, password, **extra_fields)
    
class CustomUser(AbstractBaseUser,PermissionsMixin):
    name = models.CharField(max_length=30)
    cpf = BRCPFField(unique=True)
    is_admin = models.BooleanField(default=False)
    email = models.EmailField(max_length=40, default='', validators=[checkDns])

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    password = models.CharField(max_length=100)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name,cpf']
    class Meta:
        permissions = [
            ("only_change_own", "Pode alterar apenas o próprio registro na API."),
            ("user_list", "Pode Listar todos users na API"),
            ("user_retrieve", "Pode recuperar um registro users na API"),
            ("user_update", "Pode atualizar users na API"),
            ("user_partial_update", "Pode atualizar parcialmente users na API"),
            ("user_create", "Pode criar users na API"),
            ("user_destroy", "Pode destruir users na API"),
        ]
        managed = True

    def __str__(self):
        return self.username