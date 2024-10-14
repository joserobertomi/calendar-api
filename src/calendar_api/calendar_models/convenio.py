from django.db import models
from ..validators import *


class Convenio(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=32, validators=[validade_char_lower_than_32])
    inscricao = models.CharField(max_length=64, validators=[validade_char_lower_than_64])

    def __str__(self):
        return self.nome

    class Meta:
        permissions = [
            ("convenio_create", "Pode criar convênios"),
            ("convenio_list", "Pode listar convênios"),
            ("convenio_retrieve", "Pode recuperar um convênio"),
            ("convenio_update", "Pode atualizar convênios"),
            ("convenio_partial_update", "Pode atualizar parcialmente convênios"),
            ("convenio_destroy", "Pode destruir convênios"),
        ]
        managed = True
