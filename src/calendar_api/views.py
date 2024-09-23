from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .serializers import EnderecoSerializer
from .models import Endereco


# Create your views here.
# TODO VIEWSET --> Endereco, Paciente, Medico, HorarioAtendimento, Procedimento, Convenio, SolicitacaoAgendamento, ProfissionalProcedimento 
# TODO --> Cadastro(CREATE=post), Listagem(LIST=get), Edicao(UPDATE=update), Vizualizacao(RETRIVE=get) 

def index(request):
    return HttpResponse("Hello, worldzin estoy a implementar a view")


class EnderecoViewSet(ViewSet):

    def create(self, request): 
        # Deserializa os dados da requisição e verifica se são válidos
        serializer = EnderecoSerializer(data=request.data)
        
        # Se os dados forem válidos, cria o objeto e retorna uma resposta de sucesso
        if serializer.is_valid():
            serializer.save()  # Salva o objeto no banco de dados
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Se os dados não forem válidos, retorna uma resposta de erro com os detalhes
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        # Tenta buscar o objeto que deve ser atualizado pelo `pk`
        try:
            endereco = Endereco.objects.get(pk=pk)
        except Endereco.DoesNotExist:
            raise NotFound(detail="Endereco nao encontrado")

        # Deserializa e valida os dados recebidos
        serializer = EnderecoSerializer(endereco, data=request.data)
        
        # Se os dados forem válidos, atualiza o objeto
        if serializer.is_valid():
            serializer.save()  # Atualiza o objeto no banco de dados
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # Se os dados não forem válidos, retorna uma resposta de erro
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        queryset = Endereco.objects.all()
        serializer = EnderecoSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Endereco.objects.all()
        endereco = get_object_or_404(queryset, pk=pk)
        serializer = EnderecoSerializer(endereco)
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        # Tenta buscar o objeto que será deletado pelo `pk`
        try:
            user = Endereco.objects.get(pk=pk)
        except Endereco.DoesNotExist:
            raise NotFound(detail="User not found")

        # Se o objeto for encontrado, deleta-o
        user.delete()
        
        # Retorna uma resposta de sucesso
        return Response(status=status.HTTP_204_NO_CONTENT)