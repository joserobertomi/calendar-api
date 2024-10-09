from django.db import models
from .validators import *
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .utils.choices import BRAZIL_STATES, REGISTER_TYPES, WEEK_DAYS
# Create your models here.

class Endereco(models.Model):
    id = models.BigAutoField(primary_key=True)
    cep = models.CharField(max_length=8, validators=[validate_cep])
    rua = models.CharField(max_length=32, validators=[validade_char_lower_than_32])
    bairro = models.CharField(max_length=32, validators=[validade_char_lower_than_32])
    numero = models.IntegerField(null=True, blank=True, validators=[validate_integer])
    quadra_lote = models.CharField(null=True, blank=True, max_length=16, validators=[validade_char_lower_than_16])
    cidade = models.CharField(max_length=32, validators=[validade_char_lower_than_32])
    estado = models.CharField(max_length=2, choices=BRAZIL_STATES, validators=[validate_state])
    complemento = models.CharField(max_length=32, validators=[validade_char_lower_than_32])

    def clean(self):
        # Chama a implementação original da superclasse
        super().clean()
        # Verifica se o tempo de início é posterior ao de fim
        if not self.numero and not self.quadra_lote:
            raise ValidationError(
                _("ERROR - Um dos campos numero ou quadra e lote deve existir")
            )

    def __str__(self) -> str:
        if self.numero:
            return (f"{self.numero}, {self.bairro}, {self.cidade}")
        return (f"{self.quadra_lote}, {self.bairro}, {self.cidade}")

    class Meta:
        permissions = [
            ("endereco_list", "Pode Listar todos Enderecos na API"),
            ("endereco_retrieve", "Pode recuperar um registro Endereco na API"),
            ("endereco_update", "Pode atualizar Endereco na API"),
            ("endereco_partial_update", "Pode atualizar parcialmente Endereco na API"),
            ("endereco_create", "Pode criar Enderecos na API"),
            ("endereco_destroy", "Pode destruir Enderecos na API"), 
        ]


class Convenio(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=32, validators=[validade_char_lower_than_32])
    inscricao = models.CharField(max_length=64, validators=[validade_char_lower_than_64])

    def __str__(self) -> str:
        return self.nome

    class Meta:
        permissions = [
            ("convenio_list", "Pode Listar todos Convenios na API"),
            ("convenio_retrieve", "Pode recuperar um registro Convenio na API"),
            ("convenio_update", "Pode atualizar Convenio na API"),
            ("convenio_partial_update", "Pode atualizar parcialmente Convenio na API"),
            ("convenio_create", "Pode criar Convenio na API"),
            ("convenio_destroy", "Pode destruir Convenio na API"),
        ]


class Paciente(models.Model): 
    id = models.BigAutoField(primary_key=True) 
    nome = models.CharField(max_length=32, validators=[validade_char_lower_than_32])
    sobrenome = models.CharField(max_length=32, validators=[validade_char_lower_than_32])
    cpf = models.CharField(max_length=11, unique=True, validators=[validate_cpf])
    rg = models.CharField(max_length=9, unique=True, validators=[validate_rg])
    orgao_expeditor = models.CharField(max_length=16, validators=[validade_char_lower_than_16])
    sexo = models.CharField(max_length=1, choices=(('F', 'Feminino'), ('M', 'Masculino')))
    celular = models.CharField(max_length=11, validators=[validate_phone])
    email = models.EmailField(validators=[checkDns])
    nascimento = models.DateField(validators=[validate_date_not_130_years_later, validate_date_not_newer_than_today])
    endereco_fk = models.ForeignKey(Endereco, null=True, blank=True, on_delete=models.SET_NULL)
    convenio_fk = models.ForeignKey(Convenio, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f"{self.nome} {self.sobrenome}"

    class Meta:
        permissions = [
            ("paciente_list", "Pode Listar todos pacientes na API"),
            ("paciente_retrieve", "Pode recuperar um registro de paciente na API"),
            ("paciente_update", "Pode atualizar paciente na API"),
            ("paciente_partial_update", "Pode atualizar parcialmente um paciente na API"),
            ("paciente_create", "Pode criar paciente na API"),
            ("paciente_destroy", "Pode destruir paciente na API"),
        ]


class Profissional(models.Model):
    id = models.BigAutoField(primary_key=True) 
    nome = models.CharField(max_length=32, validators=[validade_char_lower_than_32])
    sobrenome = models.CharField(max_length=32, validators=[validade_char_lower_than_32])
    cpf = models.CharField(max_length=11, unique=True, validators=[validate_cpf])
    uf_registro = models.CharField(max_length=2, choices=BRAZIL_STATES, validators=[validate_state])
    n_registro = models.PositiveIntegerField(validators=[validate_integer, validate_grater_than_1])
    tipo_registro = models.CharField(max_length=8, choices=REGISTER_TYPES, validators=[validate_registers])
    email = models.EmailField(unique=True, validators=[checkDns])

    def __str__(self) -> str:
        return f"{self.nome} {self.sobrenome}"

    class Meta:
        permissions = [
            ("profissional_list", "Pode Listar todos Profissionais na API"),
            ("profissional_retrieve", "Pode recuperar um registro Profissional na API"),
            ("profissional_update", "Pode atualizar Profissional na API"),
            ("profissional_partial_update", "Pode atualizar parcialmente Prrofissional na API"),
            ("profissional_create", "Pode criar Profissionais na API"),
            ("profissional_destroy", "Pode destruir Profissionais na API"),
        ]

class HorariosAtendimento(models.Model):
    id = models.BigAutoField(primary_key=True)
    dia_da_semana = models.CharField(choices=WEEK_DAYS, max_length=3, validators=[validate_days_of_week])
    inicio = models.TimeField()
    fim = models.TimeField()
    profissional_fk = models.ForeignKey(Profissional, null=True, on_delete=models.CASCADE)

    def clean(self):
        # Chama a implementação original da superclasse
        super().clean()

        # Verifica se o tempo de início é posterior ao de fim
        if self.inicio and self.fim and self.inicio > self.fim:
            raise ValidationError(
                _("ERROR - The finish time must be after the start time.")
            )

    def __str__(self) -> str:
        return f"{self.dia_da_semana}: {self.inicio}-{self.fim}"
    
    class Meta:
        permissions = [
            ("horario_atendimento_list", "Pode Listar todos Horarios de atendimento na API"),
            ("horario_atendimento_retrieve", "Pode recuperar um registro Horarios de atendimento na API"),
            ("horario_atendimento_update", "Pode atualizar Horarios de atendimento na API"),
            ("horario_atendimento_partial_update", "Pode atualizar parcialmente Horarios de atendimento na API"),
            ("horario_atendimento_create", "Pode criar Horarios de atendimento na API"),
            ("horario_atendimento_destroy", "Pode destruir Horarios de atendimento na API"),
        ]


class Procedimento(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=128, validators=[validade_char_lower_than_128], unique=True)
    def __str__(self) -> str:
        return self.nome
    
    class Meta:
        permissions = [
            ("procedimento_list", "Pode Listar todos procedimentos na API"),
            ("procedimento_retrieve", "Pode recuperar um registro procedimentos na API"),
            ("procedimento_update", "Pode atualizar procedimentos na API"),
            ("procedimento_partial_update", "Pode atualizar parcialmente procedimentos na API"),
            ("procedimento_create", "Pode criar procedimentos na API"),
            ("procedimento_destroy", "Pode destruir procedimentos na API"),
        ]


class ProfissionalProcedimento(models.Model):
    id = models.BigAutoField(primary_key=True)
    profissional_fk = models.ForeignKey(Profissional, null=True, on_delete=models.CASCADE)
    procedimento_fk = models.ForeignKey(Procedimento, null=True, on_delete=models.SET_NULL)
    tempo_duracao = models.DurationField()

    def __str__(self) -> str:
        return f"{self.procedimento_fk} {self.profissional_fk}"
    
    class Meta:
        permissions = [
            ("profissional_procedimento_list", "Pode Listar todos Profissional_procedimento na API"),
            ("profissional_procedimento_retrieve", "Pode recuperar um registro Profissional_procedimento na API"),
            ("profissional_procedimento_update", "Pode atualizar Profissional_procedimento na API"),
            ("profissional_procedimento_partial_update", "Pode atualizar parcialmente Profissional_procedimento na API"),
            ("profissional_procedimento_create", "Pode criar Profissional_procedimento na API"),
            ("profissional_procedimento_destroy", "Pode destruir Profissional_procedimento na API"),
        ]


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
    
    class Meta:
        permissions = [
            ("solicitacao_agendamento_list", "Pode Listar todos Solicitacao_agendamento na API"),
            ("solicitacao_agendamento_retrieve", "Pode recuperar um registro Solicitacao_agendamento na API"),
            ("solicitacao_agendamento_update", "Pode atualizar Solicitacao_agendamento na API"),
            ("solicitacao_agendamento_partial_update", "Pode atualizar parcialmente Solicitacao_agendamento na API"),
            ("solicitacao_agendamento_create", "Pode criar Solicitacao_agendamento na API"),
            ("solicitacao_agendamento_destroy", "Pode destruir Solicitacao_agendamento na API"),
        ]


class Prontuario(models.Model): 
    texto =  models.TextField()
    profissional_fk =  models.ForeignKey(Profissional, on_delete=models.CASCADE)
    paciente_fk =  models.ForeignKey(Paciente, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Prontuario: Dr(a) {self.profissional_fk} - Paciente {self.paciente_fk}"
    
    class Meta:
        permissions = [
            ("prontuario_list", "Pode Listar todos prontuarios na API"),
            ("prontuario_retrieve", "Pode recuperar um registro prontuario na API"),
            ("prontuario_update", "Pode atualizar Prontuario na API"),
            ("prontuario_partial_update", "Pode atualizar parcialmente Prontuario na API"),
            ("prontuario_create", "Pode criar Prontuario na API"),
            ("prontuario_destroy", "Pode destruir Prontuario na API"),
        ]
