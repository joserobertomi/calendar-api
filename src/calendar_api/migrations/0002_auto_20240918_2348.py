# Generated by Django 3.2 on 2024-09-19 02:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calendar_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='endereco',
            name='numero',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='endereco',
            name='quadra_lote',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='horariosatendimento',
            name='dia_da_semana',
            field=models.CharField(choices=[('2a', 'Segunda-feira'), ('3a', 'Terça-feira'), ('4a', 'Quarta-feira'), ('5a', 'Quinta-feira'), ('6a', 'Sexta-feira'), ('Sab', 'Sábado'), ('Dom', 'Domingo')], max_length=3),
        ),
        migrations.AlterField(
            model_name='horariosatendimento',
            name='profissional_fk',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='calendar_api.profissional'),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='cpf',
            field=models.CharField(max_length=11, unique=True),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='rg',
            field=models.CharField(max_length=9, unique=True),
        ),
        migrations.AlterField(
            model_name='profissional',
            name='cpf',
            field=models.CharField(max_length=11, unique=True),
        ),
        migrations.AlterField(
            model_name='profissionalprocedimento',
            name='profissional_fk',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='calendar_api.profissional'),
        ),
        migrations.AlterField(
            model_name='solicitacaoagendamento',
            name='envio_confirmacao',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solicitacaoagendamento',
            name='hora_fim_consulta',
            field=models.TimeField(blank=True, default=None, null=True),
        ),
    ]
