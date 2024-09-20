from django.db import models
from .validators import *

# Create your models here.

class Endereco(models.Model):
    BRAZIL_STATES = (
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
    )
    
    id = models.BigAutoField(primary_key=True)
    cep = models.CharField(max_length=8, validators=[validate_cep])
    rua = models.CharField(max_length=32, validators=[validade_char_lower_than_32])
    bairro = models.CharField(max_length=32, validators=[validade_char_lower_than_32])
    numero = models.IntegerField(null=True, blank=True, validators=[validate_integer])
    quadra_lote = models.CharField(null=True, blank=True, max_length=16, validators=[validade_char_lower_than_16])
    cidade = models.CharField(max_length=32, validators=[validade_char_lower_than_32])
    estado = models.CharField(max_length=2, choices=BRAZIL_STATES, validators=[validate_state])
    complemento = models.CharField(max_length=32, validators=[validade_char_lower_than_32])

    def __str__(self) -> str:
        return (f"{self.cep}, {self.cidade}, {self.estado}")


class Convenio(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=32, validators=[validade_char_lower_than_32])
    inscricao = models.CharField(max_length=64, validators=[validade_char_lower_than_64])

    def __str__(self) -> str:
        return self.nome


class Paciente(models.Model): 
    id = models.BigAutoField(primary_key=True) 
    nome = models.CharField(max_length=32, validators=[validade_char_lower_than_32])
    sobrenome = models.CharField(max_length=32, validators=[validade_char_lower_than_32])
    nome_social = models.CharField(max_length=32, null=True, blank=True, validators=[validade_char_lower_than_32])
    cpf = models.CharField(max_length=11, unique=True, validators=[validate_cpf])
    rg = models.CharField(max_length=9, unique=True, validators=[validate_rg])
    orgao_expeditor = models.CharField(max_length=16, validators=[validade_char_lower_than_16])
    sexo = models.CharField(max_length=1, choices=(('F', 'Feminino'), ('M', 'Masculino')), validators=[validate_sex])
    celular = models.CharField(max_length=11, validators=[validate_phone])
    email = models.EmailField()
    nascimento = models.DateField(validators=[validate_date_format, validate_date_not_130_years_later, validate_date_not_newer_than_today])
    endereco_fk = models.ForeignKey(Endereco, null=True, blank=True, on_delete=models.SET_NULL)
    convenio_fk = models.ForeignKey(Convenio, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f"{self.nome_social if self.nome_social else self.nome} {self.sobrenome}"


class Profissional(models.Model):
    BRAZIL_STATES = (
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
    )
    REGISTER_TYPES = (
        ('CRM', 'Conselho Regional de Medicina'),
        ('CRBM', 'Conselho Regional de Biomedicina'),
        ('CRO', 'Conselho Regional de Odontologia'),
        ('COREN', 'Conselho Regional de Enfermagem'),
        ('CRF', 'Conselho Regional de Farmácia'),
        ('CRN', 'Conselho Regional de Nutrição')
    )
    
    id = models.BigAutoField(primary_key=True) 
    nome = models.CharField(max_length=32, validators=[validade_char_lower_than_32])
    sobrenome = models.CharField(max_length=32, validators=[validade_char_lower_than_32])
    cpf = models.CharField(max_length=11, unique=True, validators=[validate_cpf])
    uf_registro = models.CharField(max_length=2, choices=BRAZIL_STATES, validators=[validate_state])
    n_registro = models.PositiveIntegerField(validators=[validate_integer, validate_grater_than_1])
    tipo_registro = models.CharField(max_length=8, choices=REGISTER_TYPES, validators=[validate_registers])
    email = models.EmailField(unique=True)

    def __str__(self) -> str:
        return f"{self.nome} {self.sobrenome}"


class HorariosAtendimento(models.Model):
    id = models.BigAutoField(primary_key=True)
    WEEK_DAYS = (
        ('2a', 'Segunda-feira'),
        ('3a', 'Terça-feira'),
        ('4a', 'Quarta-feira'),
        ('5a', 'Quinta-feira'),
        ('6a', 'Sexta-feira'),
        ('Sab', 'Sábado'),
        ('Dom', 'Domingo'),
    )

    dia_da_semana = models.CharField(choices=WEEK_DAYS, max_length=3, validators=[validate_days_of_week])
    inicio = models.TimeField(validators=[validate_time_format])
    fim = models.TimeField(validators=[validate_time_format])
    profissional_fk = models.ForeignKey(Profissional, null=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.dia_da_semana}:{self.inicio}-{self.fim}"


class Procedimento(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=32, validators=[validade_char_lower_than_32])

    def __str__(self) -> str:
        return self.nome


class ProfissionalProcedimento(models.Model):
    id = models.BigAutoField(primary_key=True)
    profissional_fk = models.ForeignKey(Profissional, null=True, on_delete=models.CASCADE)
    procedimento_fk = models.ForeignKey(Procedimento, null=True, on_delete=models.SET_NULL)
    tempo_duracao = models.DurationField(validators=validate_duration)

    def __str__(self) -> str:
        return f"{self.procedimento_fk} {self.profissional_fk}"


class SolicitacaoAgendamento(models.Model):
    STATUS_OPTIONS = (
        (1, "Aguardando ambas confirmações"),
        (2, "Aguardando confirmação do médico"), 
        (3, "Aguardando confirmação do paciente"),
        (4, "Agendamento confirmado"),
        (5, "Agendamento cancelado"),
    )
    
    id = models.BigAutoField(primary_key=True)
    data_consulta = models.DateField(validators=[validate_date_format])
    hora_inicio_consulta = models.TimeField(validators=[validate_time_format])
    hora_fim_consulta = models.TimeField(blank=True, null=True, default=None) # * CALCULADO
    envio_confirmacao_paciente = models.DateTimeField(blank=True, null=True) # * CALCULADO
    confirmacao_profissional = models.DateTimeField(null=True, default=None) # * ATRIBUIDO PELO SISTEMA 
    confirmacao_paciente = models.DateTimeField(null=True, default=None) # * ATRIBUIDO PELO SISTEMA
    status = models.SmallIntegerField(choices=STATUS_OPTIONS, default=1) # * ATRIBUIDO PELO SISTEMA
    profissional_fk = models.ForeignKey(Profissional, null=True, on_delete=models.SET_NULL)
    procedimento_fk = models.ForeignKey(Procedimento, null=True, on_delete=models.SET_NULL)
    paciente_fk = models.ForeignKey(Paciente, null=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f"{self.data_consulta}-{self.paciente_fk}-{self.profissional_fk}"