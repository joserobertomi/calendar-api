from django.contrib import admin

# Register your models here.

from .models import Endereco, Convenio, Paciente, SolicitacaoAgendamento, Profissional, ProfissionalProcedimento, Procedimento, HorariosAtendimento, Prontuario

# Registre os modelos no Django Admin
admin.site.register(Endereco)
admin.site.register(Convenio)
admin.site.register(Paciente)
admin.site.register(SolicitacaoAgendamento)
admin.site.register(Profissional)
admin.site.register(ProfissionalProcedimento)
admin.site.register(Procedimento)
admin.site.register(HorariosAtendimento)
admin.site.register(Prontuario)