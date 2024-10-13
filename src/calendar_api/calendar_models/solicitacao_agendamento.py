from django.db import models

from .paciente import Paciente
from .procedimento import Procedimento
from .profissional import Profissional
from ..validators import *


class SolicitacaoAgendamento(models.Model):
    
    id = models.BigAutoField(primary_key=True)
    data_consulta = models.DateField()
    hora_inicio_consulta = models.TimeField()
    #hora_fim_consulta = models.TimeField(blank=True, null=True, default=None) # * PROPERTY
    #envio_confirmacao_paciente = models.DateTimeField(blank=True, null=True) # * PROPERTY
    profissional_fk = models.ForeignKey(Profissional, null=True, on_delete=models.SET_NULL)
    procedimento_fk = models.ForeignKey(Procedimento, null=True, on_delete=models.SET_NULL)
    paciente_fk = models.ForeignKey(Paciente, null=True, on_delete=models.SET_NULL)

    # TODO fazer o hora_fim_consulta como propertys da classe
    @property
    def hora_fim_consulta(self):
        duracao = ProfissionalProcedimento.objects.filter(
            profissional_fk=self.profissional_fk, 
            procedimento_fk=self.procedimento_fk,
        ).values('tempo_duracao').first()['tempo_duracao']
        
        return self.hora_inicio_consulta + duracao
    
    def __str__(self) -> str:
        return f"{self.data_consulta} - {self.paciente_fk} - {self.profissional_fk}"