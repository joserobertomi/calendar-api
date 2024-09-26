from rest_framework import viewsets
from .serializers import EnderecoSerializer, ConvenioSerializer, PacienteSerializer, SolicitacaoAgendamentoSerializer, ProfissionalSerializer, ProfissionalProcedimentoSerializer, ProcedimentoSerializer, HorariosAtendimentoSerializer
from .models import Endereco, Convenio, Paciente, SolicitacaoAgendamento, Profissional, ProfissionalProcedimento, Procedimento, HorariosAtendimento


# Create your views here.

class EnderecoViewSet(viewsets.ModelViewSet):
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer


class ConvenioViewSet(viewsets.ModelViewSet):
    queryset = Convenio.objects.all()
    serializer_class = ConvenioSerializer


class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer


class SolicitacaoAgendamentoViewSet(viewsets.ModelViewSet):
    queryset = SolicitacaoAgendamento.objects.all()
    serializer_class = SolicitacaoAgendamentoSerializer


class ProfissionalViewSet(viewsets.ModelViewSet):
    queryset = Profissional.objects.all()
    serializer_class = ProfissionalSerializer


class ProfissionalProcedimentoViewSet(viewsets.ModelViewSet):
    queryset = ProfissionalProcedimento.objects.all()
    serializer_class = ProfissionalProcedimentoSerializer


class ProcedimentoViewSet(viewsets.ModelViewSet):
    queryset = Procedimento.objects.all()
    serializer_class = ProcedimentoSerializer


class HorariosAtendimentoViewSet(viewsets.ModelViewSet):
    queryset = HorariosAtendimento.objects.all()
    serializer_class = HorariosAtendimentoSerializer
