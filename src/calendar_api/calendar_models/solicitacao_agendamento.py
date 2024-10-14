from django.db import models
from .profissional_procedimento import ProfissionalProcedimento
from .paciente import Paciente
from .procedimento import Procedimento
from .profissional import Profissional
from ..validators import *

class SolicitacaoAgendamento(models.Model):
    id = models.BigAutoField(primary_key=True)
    data_consulta = models.DateField()
    hora_inicio_consulta = models.TimeField()
    profissional_fk = models.ForeignKey(Profissional, null=True, on_delete=models.SET_NULL)
    procedimento_fk = models.ForeignKey(Procedimento, null=True, on_delete=models.SET_NULL)
    paciente_fk = models.ForeignKey(Paciente, null=True, on_delete=models.SET_NULL)

    @property
    def hora_fim_consulta(self):
        duracao = ProfissionalProcedimento.objects.filter(
            profissional_fk=self.profissional_fk, 
            procedimento_fk=self.procedimento_fk,
        ).values('tempo_duracao').first()['tempo_duracao']
        
        return self.hora_inicio_consulta + duracao

    def __str__(self):
        return f"{self.data_consulta} - {self.paciente_fk} - {self.profissional_fk}"

    class Meta:
        permissions = [
            ("solicitacao_agendamento_create", "Pode criar solicitações de agendamento"),
            ("solicitacao_agendamento_list", "Pode listar solicitações de agendamento"),
            ("solicitacao_agendamento_retrieve", "Pode recuperar uma solicitação de agendamento"),
            ("solicitacao_agendamento_update", "Pode atualizar solicitações de agendamento"),
            ("solicitacao_agendamento_partial_update", "Pode atualizar parcialmente solicitações de agendamento"),
            ("solicitacao_agendamento_destroy", "Pode destruir solicitações de agendamento"),
        ]
        managed = True
