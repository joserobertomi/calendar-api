from rest_framework import viewsets
from .serializers import EnderecoSerializer, ConvenioSerializer, PacienteSerializer, SolicitacaoAgendamentoSerializer, ProfissionalSerializer, ProfissionalProcedimentoSerializer, ProcedimentoSerializer, HorariosAtendimentoSerializer, ProntuarioSerializer
from .models import Endereco, Convenio, Paciente, SolicitacaoAgendamento, Profissional, ProfissionalProcedimento, Procedimento, HorariosAtendimento, Prontuario
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsAdminOnly

# Create your views here.

class EnderecoViewSet(viewsets.ModelViewSet): 
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]



class ConvenioViewSet(viewsets.ModelViewSet): 
    queryset = Convenio.objects.all()
    serializer_class = ConvenioSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class PacienteViewSet(viewsets.ModelViewSet): 
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class SolicitacaoAgendamentoViewSet(viewsets.ModelViewSet): 
    queryset = SolicitacaoAgendamento.objects.all()
    serializer_class = SolicitacaoAgendamentoSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
        

class ProfissionalViewSet(viewsets.ModelViewSet): 
    queryset = Profissional.objects.all()
    serializer_class = ProfissionalSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class ProfissionalProcedimentoViewSet(viewsets.ModelViewSet): 
    queryset = ProfissionalProcedimento.objects.all()
    serializer_class = ProfissionalProcedimentoSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class ProcedimentoViewSet(viewsets.ModelViewSet): 
    queryset = Procedimento.objects.all()
    serializer_class = ProcedimentoSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class HorariosAtendimentoViewSet(viewsets.ModelViewSet):
    queryset = HorariosAtendimento.objects.all()
    serializer_class = HorariosAtendimentoSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    

class ProntuarioViewSet(viewsets.ModelViewSet):
    queryset = Prontuario.objects.all()
    serializer_class = ProcedimentoSerializer

    def get_permissions(self):
        permission_classes = [IsAdminOnly]
        return [permission() for permission in permission_classes]
