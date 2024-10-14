from django.db import models
from .paciente import Paciente
from .profissional import Profissional
from ..validators import *

class Prontuario(models.Model): 
    texto = models.TextField()
    profissional_fk = models.ForeignKey(Profissional, on_delete=models.CASCADE)
    paciente_fk = models.ForeignKey(Paciente, on_delete=models.CASCADE)

    def __str__(self):
        return f"Prontuario: Dr(a) {self.profissional_fk} - Paciente {self.paciente_fk}"

    class Meta:
        permissions = [
            ("prontuario_create", "Pode criar prontuários"),
            ("prontuario_list", "Pode listar prontuários"),
            ("prontuario_retrieve", "Pode recuperar um prontuário"),
            ("prontuario_update", "Pode atualizar prontuários"),
            ("prontuario_partial_update", "Pode atualizar parcialmente prontuários"),
            ("prontuario_destroy", "Pode destruir prontuários"),
        ]
        managed = True
