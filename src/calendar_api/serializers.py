from rest_framework import serializers
from .models import Endereco, CustomUser, Convenio, Paciente, SolicitacaoAgendamento, Profissional, ProfissionalProcedimento, Procedimento, HorariosAtendimento, Prontuario
from django.core.exceptions import ValidationError
import django.contrib.auth.password_validation as validators

class UserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(
        write_only=True,
        required=False,
        style={'input_type': 'password'}
    )

    class Meta:
        model = CustomUser
        fields = ['id','name','email','cpf','created_at','password']
        read_only_fields = ['id', 'created_at']
        
    def validate_password(self, value):
        if not value:
            return value
        
        try:
            validators.validate_password(value)
        except ValidationError as error:
            raise serializers.ValidationError(list(error.messages))
        return value
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password) 

        instance.save()
        return instance

        
class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = '__all__'
    read_only_fields = ['id']


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
    read_only_fields = ['id']



class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'
    read_only_fields = ['id']



class SolicitacaoAgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitacaoAgendamento
        fields = '__all__'
    read_only_fields = ['id']



class ProfissionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profissional
        fields = '__all__'
    read_only_fields = ['id']


class ProfissionalProcedimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfissionalProcedimento
        fields = '__all__'
    read_only_fields = ['id']



class ProcedimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedimento
        fields = '__all__'
    read_only_fields = ['id']



class HorariosAtendimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HorariosAtendimento
        fields = '__all__'
    read_only_fields = ['id']



class ProntuarioSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Prontuario
        fields = '__all__'
    read_only_fields = ['id']
