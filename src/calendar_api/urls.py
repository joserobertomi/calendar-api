from rest_framework.routers import DefaultRouter
from django.urls import re_path, path
from django.conf.urls import include
from rest_framework_simplejwt .views import TokenObtainPairView, TokenRefreshView, TokenVerifyView 


from .views import (
    EnderecoViewSet, 
    ConvenioViewSet, 
    PacienteViewSet, 
    SolicitacaoAgendamentoViewSet, 
    ProfissionalViewSet, 
    ProfissionalProcedimentoViewSet, 
    ProcedimentoViewSet, 
    HorariosAtendimentoViewSet, 
    ProntuarioViewSet, 
)

# Cria o roteador padrão
router = DefaultRouter()

# Registra os ViewSets no roteador
router.register(r'enderecos', EnderecoViewSet)
router.register(r'convenios', ConvenioViewSet)
router.register(r'pacientes', PacienteViewSet)
router.register(r'solicitacoes-agendamento', SolicitacaoAgendamentoViewSet)
router.register(r'profissionais', ProfissionalViewSet)
router.register(r'profissionais-procedimentos', ProfissionalProcedimentoViewSet)
router.register(r'procedimentos', ProcedimentoViewSet)
router.register(r'horarios-atendimento', HorariosAtendimentoViewSet)
router.register(r'prontuario', ProntuarioViewSet)

# Inclui as URLs geradas pelo roteador no padrão de rotas da aplicação
urlpatterns = [
    re_path('', include(router.urls)), 

    # URLS JWT  
    path('jwt/create/', TokenObtainPairView.as_view(), name='jwt_create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt_verify'), 
]