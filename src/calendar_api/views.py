from rest_framework import viewsets
from .serializers import EnderecoSerializer,UserSerializer, ConvenioSerializer, PacienteSerializer, SolicitacaoAgendamentoSerializer, ProfissionalSerializer, ProfissionalProcedimentoSerializer, ProcedimentoSerializer, HorariosAtendimentoSerializer, ProntuarioSerializer
from .models import Endereco, Convenio, Paciente,CustomUser, SolicitacaoAgendamento, Profissional, ProfissionalProcedimento, Procedimento, HorariosAtendimento, Prontuario
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import *
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.contrib.auth.models import Group
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    ordering = ['id']
    
    action_permissions = {
        'create': [AllowAny],
        'retrieve': ['calendar_api.user_retrieve'],
        'update': ['calendar_api.user_update',IsOnlyAllowedToChangeOwn],
        'partial_update': ['calendar_api.user_partial_update',IsOnlyAllowedToChangeOwn],
        'list': ['calendar_api.user_list'], 
        'destroy': ['calendar_api.user_destroy'],
    }
    
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        permission_classes = self.action_permissions.get(self.action,[])
        if not self.action == 'create':
            permission_classes += api_settings.DEFAULT_PERMISSION_CLASSES

        permission_list = []
        for permission in permission_classes:
            if isinstance(permission, str):
                if not self.request.user.has_perm(permission):
                    self.permission_denied(self.request, message=f"Voce nao tem permissao para {self.action}.")
            else:
                permission_list.append(permission())

        return permission_list

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        CustomUser.objects.create_user(
            password=serializer.validated_data.pop('password'),
            **serializer.validated_data
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, instance,*args, **kwargs):
        return Response({"message":"Voce nao pode deletar esse usuario"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsStaff])
    def change_group(self, request, pk=None):
        """
        Altera o grupo do usuário para 'profissional' ou 'padrão'.
        Apenas administradores (staff) podem acessar essa rota.
        """
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response({"detail": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Verifica o grupo atual e alterna
        professional_group = Group.objects.get(name='Profissional')
        default_group = Group.objects.get(name='Padrao')

        if professional_group in user.groups.all():
            user.groups.remove(professional_group)
            user.groups.add(default_group)
            return Response({"detail": f"Usuário {user.email} alterado para grupo 'padrão'."})
        else:
            user.groups.remove(default_group)
            user.groups.add(professional_group)
            return Response({"detail": f"Usuário {user.email} alterado para grupo 'profissional'."})
    

class EnderecoViewSet(viewsets.ModelViewSet):
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    ordering = ['id']
    
    action_permissions = {
        'create': ['calendar_api.endereco_create'],
        'retrieve': ['calendar_api.endereco_retrieve'],
        'update': ['calendar_api.endereco_update'],
        'partial_update': ['calendar_api.endereco_partial_update'],
        'list': ['calendar_api.endereco_list'],
        'destroy': ['calendar_api.endereco_destroy'],
    }

    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        permission_classes = self.action_permissions.get(self.action, [])
        permission_classes += api_settings.DEFAULT_PERMISSION_CLASSES

        permission_list = []
        for permission in permission_classes:
            if isinstance(permission, str):
                if not self.request.user.has_perm(permission):
                    self.permission_denied(self.request, message=f"Você nao tem permissao para{self.action}.")
            else:
                permission_list.append(permission())

        return permission_list


class ConvenioViewSet(viewsets.ModelViewSet):
    queryset = Convenio.objects.all()
    serializer_class = ConvenioSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    ordering = ['id']
    
    action_permissions = {
        'create': ['calendar_api.convenio_create'],
        'retrieve': ['calendar_api.convenio_retrieve'],
        'update': ['calendar_api.convenio_update'],
        'partial_update': ['calendar_api.convenio_partial_update'],
        'list': ['calendar_api.convenio_list'],
        'destroy': ['calendar_api.convenio_destroy'],
    }

    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        permission_classes = self.action_permissions.get(self.action, [])
        permission_classes += api_settings.DEFAULT_PERMISSION_CLASSES

        permission_list = []
        for permission in permission_classes:
            if isinstance(permission, str):
                if not self.request.user.has_perm(permission):
                    self.permission_denied(self.request, message=f"Você nao tem permissao para{self.action}.")
            else:
                permission_list.append(permission())

        return permission_list

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    ordering = ['id']
    
    action_permissions = {
        'create': ['calendar_api.paciente_create'],
        'retrieve': ['calendar_api.paciente_retrieve'],
        'update': ['calendar_api.paciente_update'],
        'partial_update': ['calendar_api.paciente_partial_update'],
        'list': ['calendar_api.paciente_list'],
        'destroy': ['calendar_api.paciente_destroy'],
    }

    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        permission_classes = self.action_permissions.get(self.action, [])
        permission_classes += api_settings.DEFAULT_PERMISSION_CLASSES

        permission_list = []
        for permission in permission_classes:
            if isinstance(permission, str):
                if not self.request.user.has_perm(permission):
                    self.permission_denied(self.request, message=f"Você nao tem permissao para{self.action}.")
            else:
                permission_list.append(permission())

        return permission_list


class SolicitacaoAgendamentoViewSet(viewsets.ModelViewSet):
    queryset = SolicitacaoAgendamento.objects.all()
    serializer_class = SolicitacaoAgendamentoSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    ordering = ['id']
    
    action_permissions = {
        'create': ['calendar_api.solicitacao_agendamento_create'],
        'retrieve': ['calendar_api.solicitacao_agendamento_retrieve'],
        'update': ['calendar_api.solicitacao_agendamento_update'],
        'partial_update': ['calendar_api.solicitacao_agendamento_partial_update'],
        'list': ['calendar_api.solicitacao_agendamento_list'],
        'destroy': ['calendar_api.solicitacao_agendamento_destroy'],
    }

    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        permission_classes = self.action_permissions.get(self.action, [])
        permission_classes += api_settings.DEFAULT_PERMISSION_CLASSES

        permission_list = []
        for permission in permission_classes:
            if isinstance(permission, str):
                if not self.request.user.has_perm(permission):
                    self.permission_denied(self.request, message=f"Você nao tem permissao para{self.action}.")
            else:
                permission_list.append(permission())

        return permission_list


class ProfissionalViewSet(viewsets.ModelViewSet):
    queryset = Profissional.objects.all()
    serializer_class = ProfissionalSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    ordering = ['id']
    
    action_permissions = {
        'create': ['calendar_api.profissional_create'],
        'retrieve': ['calendar_api.profissional_retrieve'],
        'update': ['calendar_api.profissional_update'],
        'partial_update': ['calendar_api.profissional_partial_update'],
        'list': ['calendar_api.profissional_list'],
        'destroy': ['calendar_api.profissional_destroy'],
    }

    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        permission_classes = self.action_permissions.get(self.action, [])
        permission_classes += api_settings.DEFAULT_PERMISSION_CLASSES

        permission_list = []
        for permission in permission_classes:
            if isinstance(permission, str):
                if not self.request.user.has_perm(permission):
                    self.permission_denied(self.request, message=f"Você nao tem permissao para{self.action}.")
            else:
                permission_list.append(permission())

        return permission_list


class ProfissionalProcedimentoViewSet(viewsets.ModelViewSet):
    queryset = ProfissionalProcedimento.objects.all()
    serializer_class = ProfissionalProcedimentoSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    ordering = ['id']
    
    action_permissions = {
        'create': ['calendar_api.profissionalprocedimento_create'],
        'retrieve': ['calendar_api.profissionalprocedimento_retrieve'],
        'update': ['calendar_api.profissionalprocedimento_update'],
        'partial_update': ['calendar_api.profissionalprocedimento_partial_update'],
        'list': ['calendar_api.profissionalprocedimento_list'],
        'destroy': ['calendar_api.profissionalprocedimento_destroy'],
    }

    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        permission_classes = self.action_permissions.get(self.action, [])
        permission_classes += api_settings.DEFAULT_PERMISSION_CLASSES

        permission_list = []
        for permission in permission_classes:
            if isinstance(permission, str):
                if not self.request.user.has_perm(permission):
                    self.permission_denied(self.request, message=f"Você nao tem permissao para{self.action}.")
            else:
                permission_list.append(permission())

        return permission_list

class ProcedimentoViewSet(viewsets.ModelViewSet):
    queryset = Procedimento.objects.all()
    serializer_class = ProcedimentoSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    ordering = ['id']
    
    action_permissions = {
        'create': ['calendar_api.procedimento_create'],
        'retrieve': ['calendar_api.procedimento_retrieve'],
        'update': ['calendar_api.procedimento_update'],
        'partial_update': ['calendar_api.procedimento_partial_update'],
        'list': ['calendar_api.procedimento_list'],
        'destroy': ['calendar_api.procedimento_destroy'],
    }

    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        permission_classes = self.action_permissions.get(self.action, [])
        permission_classes += api_settings.DEFAULT_PERMISSION_CLASSES

        permission_list = []
        for permission in permission_classes:
            if isinstance(permission, str):
                if not self.request.user.has_perm(permission):
                    self.permission_denied(self.request, message=f"Você nao tem permissao para{self.action}.")
            else:
                permission_list.append(permission())

        return permission_list

class HorariosAtendimentoViewSet(viewsets.ModelViewSet):
    queryset = HorariosAtendimento.objects.all()
    serializer_class = HorariosAtendimentoSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    ordering = ['id']
    
    action_permissions = {
        'create': ['calendar_api.horariosatendimento_create'],
        'retrieve': ['calendar_api.horariosatendimento_retrieve'],
        'update': ['calendar_api.horariosatendimento_update'],
        'partial_update': ['calendar_api.horariosatendimento_partial_update'],
        'list': ['calendar_api.horariosatendimento_list'],
        'destroy': ['calendar_api.horariosatendimento_destroy'],
    }

    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        permission_classes = self.action_permissions.get(self.action, [])
        permission_classes += api_settings.DEFAULT_PERMISSION_CLASSES

        permission_list = []
        for permission in permission_classes:
            if isinstance(permission, str):
                if not self.request.user.has_perm(permission):
                    self.permission_denied(self.request, message=f"Você nao tem permissao para{self.action}.")
            else:
                permission_list.append(permission())

        return permission_list

class ProntuarioViewSet(viewsets.ModelViewSet):
    queryset = Prontuario.objects.all()
    serializer_class = ProntuarioSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    ordering = ['id']
    
    action_permissions = {
        'create': ['calendar_api.prontuario_create'],
        'retrieve': ['calendar_api.prontuario_retrieve'],
        'update': ['calendar_api.prontuario_update'],
        'partial_update': ['calendar_api.prontuario_partial_update'],
        'list': ['calendar_api.prontuario_list'],
        'destroy': ['calendar_api.prontuario_destroy'],
    }

    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        permission_classes = self.action_permissions.get(self.action, [])
        permission_classes += api_settings.DEFAULT_PERMISSION_CLASSES

        permission_list = []
        for permission in permission_classes:
            if isinstance(permission, str):
                if not self.request.user.has_perm(permission):
                    self.permission_denied(self.request, message=f"Você nao tem permissao para{self.action}.")
            else:
                permission_list.append(permission())

        return permission_list