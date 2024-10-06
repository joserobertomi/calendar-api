from rest_framework import serializers
from .models import Endereco, Convenio, Paciente, SolicitacaoAgendamento, Profissional, ProfissionalProcedimento, Procedimento, HorariosAtendimento, Prontuario


class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = '__all__'

    def validate(self, data):
        numero = data.get('numero')
        quadra_lote = data.get('quadra_lote')
        
        if not numero and not quadra_lote:
            raise serializers.ValidationError("ERROR - Um dos campos numero ou quadra e lote deve existir")
        
        return data


class ConvenioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Convenio
        fields = '__all__'


class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'


class SolicitacaoAgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitacaoAgendamento
        fields = '__all__'


class ProfissionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profissional
        fields = '__all__'


class ProfissionalProcedimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfissionalProcedimento
        fields = '__all__'


class ProcedimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedimento
        fields = '__all__'


class HorariosAtendimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HorariosAtendimento
        fields = '__all__'


class ProntuarioSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Prontuario
        fields = '__all__'