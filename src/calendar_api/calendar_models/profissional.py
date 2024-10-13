from django.db import models
from ..validators import *
from ..utils.choices import BRAZIL_STATES, REGISTER_TYPES

class Profissional(models.Model):
    id = models.BigAutoField(primary_key=True) 
    nome = models.CharField(max_length=32, validators=[validade_char_lower_than_32])
    sobrenome = models.CharField(max_length=32, validators=[validade_char_lower_than_32])
    cpf = models.CharField(max_length=11, unique=True, validators=[validate_cpf])
    uf_registro = models.CharField(max_length=2, choices=BRAZIL_STATES, validators=[validate_state])
    n_registro = models.PositiveIntegerField(validators=[validate_integer, validate_grater_than_1])
    tipo_registro = models.CharField(max_length=8, choices=REGISTER_TYPES, validators=[validate_registers])
    email = models.EmailField(unique=True, validators=[checkDns])

    def __str__(self) -> str:
        return f"{self.nome} {self.sobrenome}"