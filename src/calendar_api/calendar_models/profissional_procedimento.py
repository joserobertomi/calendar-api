from django.db import models

from .procedimento import Procedimento
from .profissional import Profissional
from ..validators import *


class ProfissionalProcedimento(models.Model):
    id = models.BigAutoField(primary_key=True)
    profissional_fk = models.ForeignKey(Profissional, null=True, on_delete=models.CASCADE)
    procedimento_fk = models.ForeignKey(Procedimento, null=True, on_delete=models.SET_NULL)
    tempo_duracao = models.DurationField()

    def __str__(self) -> str:
        return f"{self.procedimento_fk} {self.profissional_fk}"