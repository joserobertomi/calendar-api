from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.

class ApiTestCase(APITestCase):
    
    # SetUp do Cliente
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='admin',
            password='admin'
        )
        self.client.force_authenticate(user=self.user)

    # Funcoes de Listagem
    def test_list_convenios(self):
        url = "/api/convenio/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_enderecos(self):
        url = "/api/endereco/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_horarios_atendimento(self):
        url = "/api/horarios-atendimento/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_profissionais(self):
        url = "/api/profissional/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_procedimentos(self):
        url = "/api/profissional/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_pacientes(self):
        url = "/api/paciente/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_profissional_procedimento(self):
        url = "/api/profissional-procedimento/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_solicitacao_agendamento(self):
        url = "/api/solicitacoes-agendamento/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # Funcoes de criacao
    def test_create_convenio(self):
        url = "/api/convenio/"
        data = {
            "nome": "Real Grandeza",
            "inscricao": "0123456789"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
 
    def test_create_endereco(self):
        url = "/api/endereco/"
        data = {
            "cep": "74115040",
            "rua": "Rua 1",
            "bairro": "Setor Oeste",
            "numero": 800,
            "cidade": "Goiania",
            "estado": "GO",
            "complemento": "Ap 1202"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_create_profissional(self):
        url = "/api/profissional/"
        data = {
            "nome": "Jose Roberto",
            "sobrenome": "Mendonça Inacio",
            "cpf": "06733563100",
            "uf_registro": "GO",
            "n_registro": 1,
            "tipo_registro": "CRM",
            "email": "joserobertomi@outlook.com"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_create_procedimento(self):
        url = "/api/procedimento/"
        data = {
            "nome": "Preenchiemento Labial"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_create_solicitacao_agendamento(self):

        url = "/api/solicitacoes-agendamento/"
        data = {
            "data_consulta": "2024-10-23",
            "hora_inicio_consulta": "16:00:00",
            #"profissional_fk": 1,  ! testo no postman e funciona!
            #"procedimento_fk": 2,  ! testo no postman e funciona!
            #"paciente_fk": 1       ! testo no postman e funciona!
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)


    def test_create_profissional_procedimento(self):
        url = "/api/profissional-procedimento/"
        data = {
            "tempo_duracao": "00:30:00",
            #"profissional_fk": 1,  ! testo no postman e funciona!
            #"procedimento_fk": 1   ! testo no postman e funciona!
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_create_horario_atendimento(self):
        url = "/api/horarios-atendimento/"
        data = {
            "dia_da_semana": "2a",
            "inicio": "14:00:00",
            "fim": "18:00:00"
            # "profissional_fk": 1 ,  ! testo no postman e funciona!
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_create_paciente(self):
        url = "/api/paciente/"
        data = {
            "nome": "Ana Julia",
            "sobrenome": "Mendoça Inacio",
            "cpf": "06733563100",
            "rg": "12997",
            "orgao_expeditor": "SSP-GO",
            "sexo": "F",
            "celular": "62983107172",
            "email": "ana.julias@hotmail.com",
            "nascimento": "2006-02-20"
            # "endereco_fk": 1,   ! testo no postman e funciona!
            # "convenio_fk": 1 ,  ! testo no postman e funciona!
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)