from django.db import models
from ..validators import *
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from localflavor.br.models import BRCPFField

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O usuário deve ter um email')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        if not extra_fields.get('is_superuser', False):
            try:
                default_group = Group.objects.get(name='Padrao')
                user.groups.add(default_group)
            except Group.DoesNotExist:
                pass
            
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('O superusuário deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('O superusuário deve ter is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    
class CustomUser(AbstractBaseUser,PermissionsMixin):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    cpf = BRCPFField(unique=True)
    email = models.EmailField(max_length=40,unique=True, default='', validators=[checkDns])

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    password = models.CharField(max_length=100)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','cpf']
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
        return self.email