from django.db import models
from .procedimento import Procedimento
from .profissional import Profissional
from ..validators import *

class ProfissionalProcedimento(models.Model):
    id = models.BigAutoField(primary_key=True)
    profissional_fk = models.ForeignKey(Profissional, null=True, on_delete=models.CASCADE)
    procedimento_fk = models.ForeignKey(Procedimento, null=True, on_delete=models.SET_NULL)
    tempo_duracao = models.DurationField()

    def __str__(self):
        return f"{self.procedimento_fk} {self.profissional_fk}"

    class Meta:
        permissions = [
            ("profissionalprocedimento_create", "Pode criar profissional procedimentos"),
            ("profissionalprocedimento_list", "Pode listar profissional procedimentos"),
            ("profissionalprocedimento_retrieve", "Pode recuperar um profissional procedimento"),
            ("profissionalprocedimento_update", "Pode atualizar profissional procedimentos"),
            ("profissionalprocedimento_partial_update", "Pode atualizar parcialmente profissional procedimentos"),
            ("profissionalprocedimento_destroy", "Pode destruir profissional procedimentos"),
        ]
        managed = True
