from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import index, EnderecoViewSet  # Altere o caminho conforme necessário

# Cria uma instância do DefaultRouter
router = DefaultRouter()
# Registra o UserViewSet com o nome 'users'
router.register(r'enderecos', EnderecoViewSet, basename='endereco')


urlpatterns = [
    path('index/', index, name='index'),
    path('', include(router.urls)), # Inclui as URLs do router
]