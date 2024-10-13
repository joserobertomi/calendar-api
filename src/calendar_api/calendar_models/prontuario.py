from django.db import models

from .paciente import Paciente
from .profissional import Profissional
from ..validators import *


class Prontuario(models.Model): 
    texto =  models.TextField()
    profissional_fk =  models.ForeignKey(Profissional, on_delete=models.CASCADE)
    paciente_fk =  models.ForeignKey(Paciente, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Prontuario: Dr(a) {self.profissional_fk} - Paciente {self.paciente_fk}"