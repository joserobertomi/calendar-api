from django.db import models
from .convenio import Convenio
from .endereco import Endereco
from ..validators import *
from localflavor.br.models import BRCPFField

class Paciente(models.Model): 
    id = models.BigAutoField(primary_key=True) 
    nome = models.CharField(max_length=32, validators=[validade_char_lower_than_32])
    sobrenome = models.CharField(max_length=32, validators=[validade_char_lower_than_32])
    cpf = BRCPFField(unique=True)
    rg = models.CharField(max_length=9, unique=True, validators=[validate_rg])
    orgao_expeditor = models.CharField(max_length=16, validators=[validade_char_lower_than_16])
    sexo = models.CharField(max_length=1, choices=(('F', 'Feminino'), ('M', 'Masculino')))
    celular = models.CharField(max_length=11, validators=[validate_phone])
    email = models.EmailField(validators=[checkDns])
    nascimento = models.DateField(validators=[validate_date_not_130_years_later, validate_date_not_newer_than_today])
    endereco_fk = models.ForeignKey(Endereco, null=True, blank=True, on_delete=models.SET_NULL)
    convenio_fk = models.ForeignKey(Convenio, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"

    class Meta:
        permissions = [
            ("paciente_create", "Pode criar pacientes"),
            ("paciente_list", "Pode listar pacientes"),
            ("paciente_retrieve", "Pode recuperar um paciente"),
            ("paciente_update", "Pode atualizar pacientes"),
            ("paciente_partial_update", "Pode atualizar parcialmente pacientes"),
            ("paciente_destroy", "Pode destruir pacientes"),
        ]
        managed = True
