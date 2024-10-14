from django.db import models
from ..validators import *
from ..utils.choices import BRAZIL_STATES, REGISTER_TYPES
from localflavor.br.models import BRCPFField

class Profissional(models.Model):
    id = models.BigAutoField(primary_key=True) 
    nome = models.CharField(max_length=32, validators=[validade_char_lower_than_32])
    sobrenome = models.CharField(max_length=32, validators=[validade_char_lower_than_32])
    cpf = BRCPFField(unique=True)
    uf_registro = models.CharField(max_length=2, choices=BRAZIL_STATES, validators=[validate_state])
    n_registro = models.PositiveIntegerField(validators=[validate_integer, validate_grater_than_1])
    tipo_registro = models.CharField(max_length=8, choices=REGISTER_TYPES, validators=[validate_registers])
    email = models.EmailField(unique=True, validators=[checkDns])

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"

    class Meta:
        permissions = [
            ("profissional_create", "Pode criar profissionais"),
            ("profissional_list", "Pode listar profissionais"),
            ("profissional_retrieve", "Pode recuperar um profissional"),
            ("profissional_update", "Pode atualizar profissionais"),
            ("profissional_partial_update", "Pode atualizar parcialmente profissionais"),
            ("profissional_destroy", "Pode destruir profissionais"),
        ]
        managed = True
