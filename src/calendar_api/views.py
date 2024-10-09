from rest_framework import viewsets
from .serializers import EnderecoSerializer, ConvenioSerializer, PacienteSerializer, SolicitacaoAgendamentoSerializer, ProfissionalSerializer, ProfissionalProcedimentoSerializer, ProcedimentoSerializer, HorariosAtendimentoSerializer, ProntuarioSerializer
from .models import Endereco, Convenio, Paciente, SolicitacaoAgendamento, Profissional, ProfissionalProcedimento, Procedimento, HorariosAtendimento, Prontuario
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOnly
from rest_framework.settings import api_settings

# Create your views here.

class EnderecoViewSet(viewsets.ModelViewSet): 
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer

    action_permissions = {
        'create': ['calendar_api.endereco_create', IsAuthenticated],
        'retrieve': ['calendar_api.endereco_retrieve', IsAuthenticated],
        'update': ['calendar_api.endereco_update', IsAuthenticated],
        'partial_update': ['calendar_api.endereco_partial_update', IsAuthenticated],
        'list': ['calendar_api.endereco_list', IsAuthenticated],
        'destroy': ['calendar_api.endereco_destroy', IsAuthenticated],
    }

    def get_permissions(self):
        permission_classes = self.action_permissions.get(self.action, [])
        permission_classes += list(api_settings.DEFAULT_PERMISSION_CLASSES)

        permission_list = []
        for permission in permission_classes:
            if isinstance(permission, str):
                # Checa se o usuário tem a permissão via `has_perm()`
                if not self.request.user.has_perm(permission):
                    self.permission_denied(self.request, message=f"You do not have permission to {self.action}.")
            else:
                # Instancia a classe de permissão customizada
                permission_list.append(permission())

        return permission_list







class ConvenioViewSet(viewsets.ModelViewSet): 
    queryset = Convenio.objects.all()
    serializer_class = ConvenioSerializer

    action_permissions = {
        'create': ['calendar_api.convenio_create', IsAuthenticated],
        'retrieve': ['calendar_api.convenio_retrieve', IsAuthenticated],
        'update': ['calendar_api.convenio_update', IsAuthenticated],
        'partial_update': ['calendar_api.convenio_partial_update', IsAuthenticated],
        'list': ['calendar_api.convenio_list', IsAuthenticated],
        'destroy': ['calendar_api.convenio_destroy', IsAuthenticated],
    }

    def get_permissions(self):
        #logging.getLogger('myapp').error(f"Valor da variável:, {self.action} ")
        permission_classes = self.action_permissions.get(self.action,[])
        permission_classes += api_settings.DEFAULT_PERMISSION_CLASSES

        # Adiciona permissões customizadas e padrão
        permission_list = []
        for permission in permission_classes:
            if isinstance(permission, str):
                # Se for uma permissão do Django, checa via `has_perm()`
                if not self.request.user.has_perm(permission):
                    self.permission_denied(self.request, message=f"You do not have permission to {self.action}.")
            else:
                # Se for uma classe de permissão customizada, instancia ela
                permission_list.append(permission())

        return permission_list


class PacienteViewSet(viewsets.ModelViewSet): 
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

    action_permissions = {
        'create': ['calendar_api.paciente_create', IsAuthenticated],
        'retrieve': ['calendar_api.paciente_retrieve', IsAuthenticated],
        'update': ['calendar_api.paciente_update', IsAuthenticated],
        'partial_update': ['calendar_api.paciente_partial_update', IsAuthenticated],
        'list': ['calendar_api.paciente_list', IsAuthenticated],
        'destroy': ['calendar_api.paciente_destroy', IsAuthenticated],
    }

    def get_permissions(self):
        #logging.getLogger('myapp').error(f"Valor da variável:, {self.action} ")
        permission_classes = self.action_permissions.get(self.action,[])
        permission_classes += api_settings.DEFAULT_PERMISSION_CLASSES

        # Adiciona permissões customizadas e padrão
        permission_list = []
        for permission in permission_classes:
            if isinstance(permission, str):
                # Se for uma permissão do Django, checa via `has_perm()`
                if not self.request.user.has_perm(permission):
                    self.permission_denied(self.request, message=f"You do not have permission to {self.action}.")
            else:
                # Se for uma classe de permissão customizada, instancia ela
                permission_list.append(permission())

        return permission_list


class SolicitacaoAgendamentoViewSet(viewsets.ModelViewSet): 
    queryset = SolicitacaoAgendamento.objects.all()
    serializer_class = SolicitacaoAgendamentoSerializer

    action_permissions = {
        'create': ['calendar_api.solicitacao_agendamento_create', IsAuthenticated],
        'retrieve': ['calendar_api.solicitacao_agendamento_retrieve', IsAuthenticated],
        'update': ['calendar_api.solicitacao_agendamento_update', IsAuthenticated],
        'partial_update': ['calendar_api.solicitacao_agendamento_partial_update', IsAuthenticated],
        'list': ['calendar_api.solicitacao_agendamento_list', IsAuthenticated],
        'destroy': ['calendar_api.solicitacao_agendamento_destroy', IsAuthenticated],
    }

    def get_permissions(self):
        #logging.getLogger('myapp').error(f"Valor da variável:, {self.action} ")
        permission_classes = self.action_permissions.get(self.action,[])
        permission_classes += api_settings.DEFAULT_PERMISSION_CLASSES

        # Adiciona permissões customizadas e padrão
        permission_list = []
        for permission in permission_classes:
            if isinstance(permission, str):
                # Se for uma permissão do Django, checa via `has_perm()`
                if not self.request.user.has_perm(permission):
                    self.permission_denied(self.request, message=f"You do not have permission to {self.action}.")
            else:
                # Se for uma classe de permissão customizada, instancia ela
                permission_list.append(permission())

        return permission_list
        

class ProfissionalViewSet(viewsets.ModelViewSet): 
    queryset = Profissional.objects.all()
    serializer_class = ProfissionalSerializer

    action_permissions = {
        'create': ['calendar_api.profissional_create', IsAuthenticated],
        'retrieve': ['calendar_api.profissional_retrieve', IsAuthenticated],
        'update': ['calendar_api.profissional_update', IsAuthenticated],
        'partial_update': ['calendar_api.profissional_partial_update', IsAuthenticated],
        'list': ['calendar_api.profissional_list', IsAuthenticated],
        'destroy': ['calendar_api.profissional_destroy', IsAuthenticated],
    }

    def get_permissions(self):
        #logging.getLogger('myapp').error(f"Valor da variável:, {self.action} ")
        permission_classes = self.action_permissions.get(self.action,[])
        permission_classes += api_settings.DEFAULT_PERMISSION_CLASSES

        # Adiciona permissões customizadas e padrão
        permission_list = []
        for permission in permission_classes:
            if isinstance(permission, str):
                # Se for uma permissão do Django, checa via `has_perm()`
                if not self.request.user.has_perm(permission):
                    self.permission_denied(self.request, message=f"You do not have permission to {self.action}.")
            else:
                # Se for uma classe de permissão customizada, instancia ela
                permission_list.append(permission())

        return permission_list


class ProfissionalProcedimentoViewSet(viewsets.ModelViewSet): 
    queryset = ProfissionalProcedimento.objects.all()
    serializer_class = ProfissionalProcedimentoSerializer

    action_permissions = {
        'create': ['calendar_api.profissional_procedimento_create', IsAuthenticated],
        'retrieve': ['calendar_api.profissional_procedimento_retrieve', IsAuthenticated],
        'update': ['calendar_api.profissional_procedimento_update', IsAuthenticated],
        'partial_update': ['calendar_api.profissional_procedimento_partial_update', IsAuthenticated],
        'list': ['calendar_api.profissional_procedimento_list', IsAuthenticated],
        'destroy': ['calendar_api.profissional_procedimento_destroy', IsAuthenticated],
    }

    def get_permissions(self):
        #logging.getLogger('myapp').error(f"Valor da variável:, {self.action} ")
        permission_classes = self.action_permissions.get(self.action,[])
        permission_classes += api_settings.DEFAULT_PERMISSION_CLASSES

        # Adiciona permissões customizadas e padrão
        permission_list = []
        for permission in permission_classes:
            if isinstance(permission, str):
                # Se for uma permissão do Django, checa via `has_perm()`
                if not self.request.user.has_perm(permission):
                    self.permission_denied(self.request, message=f"You do not have permission to {self.action}.")
            else:
                # Se for uma classe de permissão customizada, instancia ela
                permission_list.append(permission())

        return permission_list


class ProcedimentoViewSet(viewsets.ModelViewSet): 
    queryset = Procedimento.objects.all()
    serializer_class = ProcedimentoSerializer

    action_permissions = {
        'create': ['calendar_api.procedimento_create', IsAuthenticated],
        'retrieve': ['calendar_api.procedimento_retrieve', IsAuthenticated],
        'update': ['calendar_api.procedimento_update', IsAuthenticated],
        'partial_update': ['calendar_api.procedimento_partial_update', IsAuthenticated],
        'list': ['calendar_api.procedimento_list', IsAuthenticated],
        'destroy': ['calendar_api.procedimento_destroy', IsAuthenticated],
    }

    def get_permissions(self):
        #logging.getLogger('myapp').error(f"Valor da variável:, {self.action} ")
        permission_classes = self.action_permissions.get(self.action,[])
        permission_classes += api_settings.DEFAULT_PERMISSION_CLASSES

        # Adiciona permissões customizadas e padrão
        permission_list = []
        for permission in permission_classes:
            if isinstance(permission, str):
                # Se for uma permissão do Django, checa via `has_perm()`
                if not self.request.user.has_perm(permission):
                    self.permission_denied(self.request, message=f"You do not have permission to {self.action}.")
            else:
                # Se for uma classe de permissão customizada, instancia ela
                permission_list.append(permission())

        return permission_list


class HorariosAtendimentoViewSet(viewsets.ModelViewSet):
    queryset = HorariosAtendimento.objects.all()
    serializer_class = HorariosAtendimentoSerializer

    action_permissions = {
        'create': ['calendar_api.horario_atendimento_create', IsAuthenticated],
        'retrieve': ['calendar_api.horario_atendimento_retrieve', IsAuthenticated],
        'update': ['calendar_api.horario_atendimento_update', IsAuthenticated],
        'partial_update': ['calendar_api.horario_atendimento_partial_update', IsAuthenticated],
        'list': ['calendar_api.horario_atendimento_list', IsAuthenticated],
        'destroy': ['calendar_api.horario_atendimento_destroy', IsAuthenticated],
    }

    def get_permissions(self):
        #logging.getLogger('myapp').error(f"Valor da variável:, {self.action} ")
        permission_classes = self.action_permissions.get(self.action,[])
        permission_classes += api_settings.DEFAULT_PERMISSION_CLASSES

        # Adiciona permissões customizadas e padrão
        permission_list = []
        for permission in permission_classes:
            if isinstance(permission, str):
                # Se for uma permissão do Django, checa via `has_perm()`
                if not self.request.user.has_perm(permission):
                    self.permission_denied(self.request, message=f"You do not have permission to {self.action}.")
            else:
                # Se for uma classe de permissão customizada, instancia ela
                permission_list.append(permission())

        return permission_list
    

class ProntuarioViewSet(viewsets.ModelViewSet):
    queryset = Prontuario.objects.all()
    serializer_class = ProntuarioSerializer
    
    action_permissions = {
        'create': ['calendar_api.prontuario_create', IsAdminOnly],
        'retrieve': ['calendar_api.prontuario_retrieve', IsAdminOnly],
        'update': ['calendar_api.prontuario_update', IsAdminOnly],
        'partial_update': ['calendar_api.prontuario_partial_update', IsAdminOnly],
        'list': ['calendar_api.prontuario_list', IsAdminOnly],
        'destroy': ['calendar_api.prontuario_destroy', IsAdminOnly],
    }

    def get_permissions(self):
        #logging.getLogger('myapp').error(f"Valor da variável:, {self.action} ")
        permission_classes = self.action_permissions.get(self.action,[])
        permission_classes += api_settings.DEFAULT_PERMISSION_CLASSES

        # Adiciona permissões customizadas e padrão
        permission_list = []
        for permission in permission_classes:
            if isinstance(permission, str):
                # Se for uma permissão do Django, checa via `has_perm()`
                if not self.request.user.has_perm(permission):
                    self.permission_denied(self.request, message=f"You do not have permission to {self.action}.")
            else:
                # Se for uma classe de permissão customizada, instancia ela
                permission_list.append(permission())

        return permission_list
