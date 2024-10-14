from django.db import models
from ..validators import *

class Procedimento(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=128, validators=[validade_char_lower_than_128], unique=True)

    def __str__(self):
        return self.nome

    class Meta:
        permissions = [
            ("procedimento_create", "Pode criar procedimentos"),
            ("procedimento_list", "Pode listar procedimentos"),
            ("procedimento_retrieve", "Pode recuperar um procedimento"),
            ("procedimento_update", "Pode atualizar procedimentos"),
            ("procedimento_partial_update", "Pode atualizar parcialmente procedimentos"),
            ("procedimento_destroy", "Pode destruir procedimentos"),
        ]
        managed = True
