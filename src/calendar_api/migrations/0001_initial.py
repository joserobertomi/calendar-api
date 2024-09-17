# Generated by Django 3.2 on 2024-09-17 03:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Convenio',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=32)),
                ('inscricao', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('cep', models.CharField(max_length=8)),
                ('rua', models.CharField(max_length=32)),
                ('bairro', models.CharField(max_length=32)),
                ('numero', models.IntegerField(null=True)),
                ('quadra_lote', models.CharField(max_length=16, null=True)),
                ('cidade', models.CharField(max_length=64)),
                ('estado', models.CharField(choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], max_length=2)),
                ('complemento', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=32)),
                ('sobrenome', models.CharField(max_length=32)),
                ('nome_social', models.CharField(blank=True, max_length=32, null=True)),
                ('cpf', models.CharField(max_length=11)),
                ('rg', models.CharField(max_length=9)),
                ('orgao_expeditor', models.CharField(max_length=16)),
                ('sexo', models.CharField(choices=[('F', 'Feminino'), ('M', 'Masculino')], max_length=1)),
                ('celular', models.CharField(max_length=11)),
                ('email', models.EmailField(max_length=254)),
                ('nascimento', models.DateField()),
                ('convenio_fk', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='calendar_api.convenio')),
                ('endereco_fk', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='calendar_api.endereco')),
            ],
        ),
        migrations.CreateModel(
            name='Procedimento',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Profissional',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=32)),
                ('sobrenome', models.CharField(max_length=32)),
                ('cpf', models.CharField(max_length=11)),
                ('uf_registro', models.CharField(choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], max_length=2)),
                ('n_registro', models.PositiveIntegerField()),
                ('tipo_registro', models.CharField(choices=[('CRM', 'Conselho Regional de Medicina'), ('CRBM', 'Conselho Regional de Biomedicina'), ('CRO', 'Conselho Regional de Odontologia'), ('COREN', 'Conselho Regional de Enfermagem'), ('CRF', 'Conselho Regional de Farmácia'), ('CRN', 'Conselho Regional de Nutrição')], max_length=8)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='SolicitacaoAgendamento',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('data_consulta', models.DateField()),
                ('hora_inicio_consulta', models.TimeField()),
                ('hora_fim_consulta', models.TimeField()),
                ('envio_confirmacao', models.DateTimeField()),
                ('confirmacao_profissional', models.DateTimeField(default=None, null=True)),
                ('confirmacao_paciente', models.DateTimeField(default=None, null=True)),
                ('status', models.SmallIntegerField(choices=[(1, 'Aguardando ambas confirmações'), (2, 'Aguardando confirmação do médico'), (3, 'Aguardando confirmação do paciente'), (4, 'Agendamento confirmado'), (5, 'Agendamento cancelado')], default=1)),
                ('paciente_fk', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='calendar_api.paciente')),
                ('procedimento_fk', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='calendar_api.procedimento')),
                ('profissional_fk', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='calendar_api.profissional')),
            ],
        ),
        migrations.CreateModel(
            name='ProfissionalProcedimento',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('tempo_duracao', models.DurationField()),
                ('procedimento_fk', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='calendar_api.procedimento')),
                ('profissional_fk', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='calendar_api.profissional')),
            ],
        ),
        migrations.CreateModel(
            name='HorariosAtendimento',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('dia_da_semana', models.SmallIntegerField(choices=[(1, 'Segunda-feira'), (2, 'Terça-feira'), (3, 'Quarta-feira'), (4, 'Quinta-feira'), (5, 'Sexta-feira'), (6, 'Sábado'), (7, 'Domingo')])),
                ('inicio', models.TimeField()),
                ('fim', models.TimeField()),
                ('profissional_fk', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='calendar_api.profissional')),
            ],
        ),
    ]
