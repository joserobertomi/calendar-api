# Generated by Django 3.2 on 2024-10-03 21:05

import calendar_api.validators
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
                ('nome', models.CharField(max_length=32, validators=[calendar_api.validators.validade_char_lower_than_32])),
                ('inscricao', models.CharField(max_length=64, validators=[calendar_api.validators.validade_char_lower_than_64])),
            ],
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('cep', models.CharField(max_length=8, validators=[calendar_api.validators.validate_cep])),
                ('rua', models.CharField(max_length=32, validators=[calendar_api.validators.validade_char_lower_than_32])),
                ('bairro', models.CharField(max_length=32, validators=[calendar_api.validators.validade_char_lower_than_32])),
                ('numero', models.IntegerField(blank=True, null=True, validators=[calendar_api.validators.validate_integer])),
                ('quadra_lote', models.CharField(blank=True, max_length=16, null=True, validators=[calendar_api.validators.validade_char_lower_than_16])),
                ('cidade', models.CharField(max_length=32, validators=[calendar_api.validators.validade_char_lower_than_32])),
                ('estado', models.CharField(choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], max_length=2, validators=[calendar_api.validators.validate_state])),
                ('complemento', models.CharField(max_length=32, validators=[calendar_api.validators.validade_char_lower_than_32])),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=32, validators=[calendar_api.validators.validade_char_lower_than_32])),
                ('sobrenome', models.CharField(max_length=32, validators=[calendar_api.validators.validade_char_lower_than_32])),
                ('cpf', models.CharField(max_length=11, unique=True, validators=[calendar_api.validators.validate_cpf])),
                ('rg', models.CharField(max_length=9, unique=True, validators=[calendar_api.validators.validate_rg])),
                ('orgao_expeditor', models.CharField(max_length=16, validators=[calendar_api.validators.validade_char_lower_than_16])),
                ('sexo', models.CharField(choices=[('F', 'Feminino'), ('M', 'Masculino')], max_length=1)),
                ('celular', models.CharField(max_length=11, validators=[calendar_api.validators.validate_phone])),
                ('email', models.EmailField(max_length=254)),
                ('nascimento', models.DateField(validators=[calendar_api.validators.validate_date_not_130_years_later, calendar_api.validators.validate_date_not_newer_than_today])),
                ('convenio_fk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='calendar_api.convenio')),
                ('endereco_fk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='calendar_api.endereco')),
            ],
        ),
        migrations.CreateModel(
            name='Procedimento',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=32, unique=True, validators=[calendar_api.validators.validade_char_lower_than_32])),
            ],
        ),
        migrations.CreateModel(
            name='Profissional',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=32, validators=[calendar_api.validators.validade_char_lower_than_32])),
                ('sobrenome', models.CharField(max_length=32, validators=[calendar_api.validators.validade_char_lower_than_32])),
                ('cpf', models.CharField(max_length=11, unique=True, validators=[calendar_api.validators.validate_cpf])),
                ('uf_registro', models.CharField(choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], max_length=2, validators=[calendar_api.validators.validate_state])),
                ('n_registro', models.PositiveIntegerField(validators=[calendar_api.validators.validate_integer, calendar_api.validators.validate_grater_than_1])),
                ('tipo_registro', models.CharField(choices=[('CRM', 'Conselho Regional de Medicina'), ('CRBM', 'Conselho Regional de Biomedicina'), ('CRO', 'Conselho Regional de Odontologia'), ('COREN', 'Conselho Regional de Enfermagem'), ('CRF', 'Conselho Regional de Farmácia'), ('CRN', 'Conselho Regional de Nutrição')], max_length=8, validators=[calendar_api.validators.validate_registers])),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SolicitacaoAgendamento',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('data_consulta', models.DateField()),
                ('hora_inicio_consulta', models.TimeField()),
                ('paciente_fk', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='calendar_api.paciente')),
                ('procedimento_fk', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='calendar_api.procedimento')),
                ('profissional_fk', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='calendar_api.profissional')),
            ],
        ),
        migrations.CreateModel(
            name='Prontuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField()),
                ('paciente_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calendar_api.paciente')),
                ('profissional_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calendar_api.profissional')),
            ],
        ),
        migrations.CreateModel(
            name='ProfissionalProcedimento',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('tempo_duracao', models.DurationField()),
                ('procedimento_fk', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='calendar_api.procedimento')),
                ('profissional_fk', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='calendar_api.profissional')),
            ],
        ),
        migrations.CreateModel(
            name='HorariosAtendimento',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('dia_da_semana', models.CharField(choices=[('2a', 'Segunda-feira'), ('3a', 'Terça-feira'), ('4a', 'Quarta-feira'), ('5a', 'Quinta-feira'), ('6a', 'Sexta-feira'), ('Sab', 'Sábado'), ('Dom', 'Domingo')], max_length=3, validators=[calendar_api.validators.validate_days_of_week])),
                ('inicio', models.TimeField()),
                ('fim', models.TimeField()),
                ('profissional_fk', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='calendar_api.profissional')),
            ],
        ),
    ]
