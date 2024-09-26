from rest_framework.routers import DefaultRouter
from .views import (
    EnderecoViewSet, 
    ConvenioViewSet, 
    PacienteViewSet, 
    SolicitacaoAgendamentoViewSet, 
    ProfissionalViewSet, 
    ProfissionalProcedimentoViewSet, 
    ProcedimentoViewSet, 
    HorariosAtendimentoViewSet
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

# Inclui as URLs geradas pelo roteador no padrão de rotas da aplicação
urlpatterns = router.urls
