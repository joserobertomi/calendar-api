from django.db import models

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
    cep = models.CharField(max_length=8)
    rua = models.CharField(max_length=32)
    bairro = models.CharField(max_length=32)
    numero = models.IntegerField(null=True, blank=True)
    quadra_lote = models.CharField(null=True, blank=True, max_length=16)
    cidade = models.CharField(max_length=64)
    estado = models.CharField(max_length=2, choices=BRAZIL_STATES)
    complemento = models.CharField(max_length=32)

    def __str__(self) -> str:
        return (f"{self.cep}, {self.cidade}, {self.estado}")


class Convenio(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=32)
    inscricao = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.nome


class Paciente(models.Model): 
    id = models.BigAutoField(primary_key=True) 
    nome = models.CharField(max_length=32)
    sobrenome = models.CharField(max_length=32)
    nome_social = models.CharField(max_length=32, null=True, blank=True)
    cpf = models.CharField(max_length=11, unique=True)
    rg = models.CharField(max_length=9, unique=True)
    orgao_expeditor = models.CharField(max_length=16)
    sexo = models.CharField(max_length=1, choices=(('F', 'Feminino'), ('M', 'Masculino')))
    celular = models.CharField(max_length=11)
    email = models.EmailField()
    nascimento = models.DateField()
    endereco_fk = models.ForeignKey(Endereco, null=True, on_delete=models.SET_NULL)
    convenio_fk = models.ForeignKey(Convenio, null=True, on_delete=models.SET_NULL)

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
    nome = models.CharField(max_length=32)
    sobrenome = models.CharField(max_length=32)
    cpf = models.CharField(max_length=11, unique=True)
    uf_registro = models.CharField(max_length=2, choices=BRAZIL_STATES)
    n_registro = models.PositiveIntegerField()
    tipo_registro = models.CharField(max_length=8, choices=REGISTER_TYPES)
    email = models.EmailField()

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

    dia_da_semana = models.CharField(choices=WEEK_DAYS, max_length=3)
    inicio = models.TimeField()
    fim = models.TimeField()
    profissional_fk = models.ForeignKey(Profissional, null=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.dia_da_semana}:{self.inicio}-{self.fim}"


class Procedimento(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=32)

    def __str__(self) -> str:
        return self.nome


class ProfissionalProcedimento(models.Model):
    id = models.BigAutoField(primary_key=True)
    profissional_fk = models.ForeignKey(Profissional, null=True, on_delete=models.CASCADE)
    procedimento_fk = models.ForeignKey(Procedimento, null=True, on_delete=models.SET_NULL)
    tempo_duracao = models.DurationField()

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
    data_consulta = models.DateField()
    hora_inicio_consulta = models.TimeField()
    hora_fim_consulta = models.TimeField(blank=True, null=True, default=None)
    envio_confirmacao = models.DateTimeField(blank=True, null=True)
    confirmacao_profissional = models.DateTimeField(null=True, default=None)
    confirmacao_paciente = models.DateTimeField(null=True, default=None)
    status = models.SmallIntegerField(choices=STATUS_OPTIONS, default=1)
    profissional_fk = models.ForeignKey(Profissional, null=True, on_delete=models.SET_NULL)
    procedimento_fk = models.ForeignKey(Procedimento, null=True, on_delete=models.SET_NULL)
    paciente_fk = models.ForeignKey(Paciente, null=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f"{self.data_consulta}-{self.paciente_fk}-{self.profissional_fk}"