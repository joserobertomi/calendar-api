from rest_framework import serializers
from .models import Endereco, Convenio, Paciente, SolicitacaoAgendamento, Profissional, ProfissionalProcedimento, Procedimento, HorariosAtendimento


class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = '__all__'