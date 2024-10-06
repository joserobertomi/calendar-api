from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Endereco, Convenio, Paciente, SolicitacaoAgendamento, Profissional, ProfissionalProcedimento, Procedimento, HorariosAtendimento, Prontuario

# Create your tests here.

class ApiTestCase(APITestCase):
    
    # SetUp do Cliente
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='admin',
            password='admin'
        )
        self.client.force_authenticate(user=self.user)

        self.profissional = Profissional.objects.create(
            nome = "Joilson", 
            sobrenome = "Jose Inacio", 
            cpf = "43326714149",
            uf_registro = "GO",
            n_registro = 1,
            tipo_registro = "CRM",
            email = "joilson@gmail.com" 
        )
        self.endereco = Endereco.objects.create(
            cep = "13479683",
            rua = "Joao Borges",
            bairro = "Jaira",
            numero = 90 ,
            cidade = "Americana",
            estado = "SP"
        )
        self.convenio = Convenio.objects.create(
            nome = "Liberty",
            inscricao = "123456"
        )
        self.procedimento = Procedimento.objects.create(
            nome = "Cirurgia de Hemorroida",
        )
        self.paciente = Paciente.objects.create(
            nome = "Adelaide Christina",
            sobrenome = "Reboucas Inacio", 
            cpf = 92708765191, 
            rg = 3791808, 
            orgao_expeditor = "SSP-GO", 
            sexo = "F", 
            celular = 62981392570,
            email = "adelaide.mundoquali@gmail.com",
            nascimento = "1986-06-25"
        )
        self.solicitacao_agendamento = SolicitacaoAgendamento.objects.create(
            data_consulta = "2024-10-30",
            hora_inicio_consulta = "16:00:00"
        )
        self.horarios_atendimento = HorariosAtendimento.objects.create(
            dia_da_semana = '2a',
            inicio = "08:00:00",
            fim = "12:00:00"
        )
        self.profissional_procedimento = ProfissionalProcedimento.objects.create(
            tempo_duracao = "00:30:00"
        )
    

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
        url = "/api/procedimento/"
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
            "profissional_fk": self.profissional.id,  
            "procedimento_fk": self.procedimento.id,  
            "paciente_fk": self.paciente.id       
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_create_profissional_procedimento(self):
        url = "/api/profissional-procedimento/"
        data = {
            "tempo_duracao": "00:30:00",
            "profissional_fk": self.profissional.id,
            "procedimento_fk": self.procedimento.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_create_horario_atendimento(self):
        url = "/api/horarios-atendimento/"
        data = {
            "dia_da_semana": "2a",
            "inicio": "14:00:00",
            "fim": "18:00:00",
            "profissional_fk": self.profissional.id
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
            "nascimento": "2006-02-20",
            "endereco_fk": self.endereco.id,
            "convenio_fk": self.convenio.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    # Fluxos de erros
    def test_erro_create_convenio_sem_convenio(self):
        url = "/api/convenio/"
        data = {
            "inscricao": "0123456"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_erro_create_convenio_sem_inscricao(self):
        url = "/api/convenio/"
        data = {
            "nome": "Real Grandeza"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_erro_create_endereco_cep_invalido(self):
        url = "/api/endereco/"
        data = {
            "cep": "74II504AA",
            "rua": "Rua 1",
            "bairro": "Setor Oeste",
            "numero": 800,
            "cidade": "Goiania",
            "estado": "GO",
            "complemento": "Ap 1202"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_erro_create_endereco_sem_numero_e_sem_quadra_lote(self):
        url = "/api/endereco/"
        data = {
            "cep": "74115040",
            "rua": "Rua 1",
            "bairro": "Setor Oeste",
            "cidade": "Goiania",
            "estado": "GO",
            "complemento": "Ap 1202"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_erro_create_endereco_sem_cidade(self):
        url = "/api/endereco/"
        data = {
            "cep": "74115040",
            "rua": "Rua 1",
            "bairro": "Setor Oeste",
            "numero": 800,
            "estado": "GO",
            "complemento": "Ap 1202"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_erro_create_endereco_estado_invalido(self):
        url = "/api/endereco/"
        data = {
            "id": 1,
            "cep": "74115040",
            "rua": "Rua 1",
            "bairro": "Setor Oeste",
            "numero": 800,
            "cidade": "Goiania",
            "estado": "PO",
            "complemento": "Ap 1202"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
    
    def test_erro_create_profissional_sem_nome(self):
        url = "/api/profissional/"
        data = {
            "sobrenome": "Mendonça Inacio",
            "cpf": "06733563100",
            "uf_registro": "GO",
            "n_registro": 1,
            "tipo_registro": "CRM",
            "email": "joserobertomi@outlook.com"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_erro_create_profissional_com_cpf_invalido(self):
        url = "/api/profissional/"
        data = {
            "nome": "Jose Roberto", 
            "sobrenome": "Mendonça Inacio",
            "cpf": "06733563101",
            "uf_registro": "GO",
            "n_registro": 1,
            "tipo_registro": "CRM",
            "email": "joserobertomi@outlook.com"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_erro_create_profissional_sem_n_registro(self):
        url = "/api/profissional/"
        data = {
            "nome": "Jose Roberto", 
            "sobrenome": "Mendonça Inacio",
            "cpf": "06733563101",
            "uf_registro": "GO",
            "tipo_registro": "CRM",
            "email": "joserobertomi@outlook.com"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_erro_create_profissional_com_n_registro_invalido(self):
        url = "/api/profissional/"
        data = {
            "nome": "Jose Roberto", 
            "sobrenome": "Mendonça Inacio",
            "cpf": "06733563101",
            "uf_registro": "GO",
            "n_registro": "A",
            "tipo_registro": "CRM",
            "email": "joserobertomi@outlook.com"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_erro_create_profissional_com_tipo_registro_invalido(self):
        url = "/api/profissional/"
        data = {
            "nome": "Jose Roberto", 
            "sobrenome": "Mendonça Inacio",
            "cpf": "06733563101",
            "uf_registro": "GO",
            "n_registro": "A",
            "tipo_registro": "CRMM",
            "email": "joserobertomi@outlook.com"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_erro_create_profissional_sem_email(self):
        url = "/api/profissional/"
        data = {
            "nome": "Jose Roberto", 
            "sobrenome": "Mendonça Inacio",
            "cpf": "06733563101",
            "uf_registro": "GO",
            "n_registro": "A",
            "tipo_registro": "CRM"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def  test_erro_create_profissional_com_email_existente(self):
        url = "/api/profissional/"
        data = {
            "nome": "Jose Roberto", 
            "sobrenome": "Mendonça Inacio",
            "cpf": "06733563101",
            "uf_registro": "GO",
            "n_registro": "A",
            "tipo_registro": "CRM",
            "email": "joilson@gmail.com"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_erro_create_procedimento_sem_dado(self):
        url = "/api/procedimento/"
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
    
    def test_erro_create_solicitacao_agendamento_formato_data_invalido(self):

        url = "/api/solicitacoes-agendamento/"
        data = {
            "data_consulta": "2024-23-12",
            "hora_inicio_consulta": "16:00:00",
            "profissional_fk": self.profissional.id,  
            "procedimento_fk": self.procedimento.id,  
            "paciente_fk": self.paciente.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
    
    def test_erro_create_solicitacao_agendamento_formato_inicio_invalido(self):

        url = "/api/solicitacoes-agendamento/"
        data = {
            "data_consulta": "2024-23-12",
            "hora_inicio_consulta": "16 horas",
            "profissional_fk": self.profissional.id,  
            "procedimento_fk": self.procedimento.id,  
            "paciente_fk": self.paciente.id    
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_erro_create_solicitacao_agendamento_data_invalida(self):

        url = "/api/solicitacoes-agendamento/"
        data = {
            "data_consulta": "2000-23-12",
            "hora_inicio_consulta": "16:00:00",
            "profissional_fk": self.profissional.id,  
            "procedimento_fk": self.procedimento.id,  
            "paciente_fk": self.paciente.id 
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_erro_create_profissional_procedimento(self):
        url = "/api/profissional-procedimento/"
        data = {
            "tempo_duracao": "30 minutos",
            "profissional_fk": self.profissional.id,  
            "procedimento_fk": self.procedimento.id,  
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_erro_create_horario_atendimento_com_formato_dia_invalido(self):
        url = "/api/horarios-atendimento/"
        data = {
            "dia_da_semana": "segunda feira",
            "inicio": "14:00:00",
            "fim": "18:00:00",
            "profissional_fk": self.profissional.id,  
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_erro_create_horario_atendimento_com_inicio_e_fim_invalido(self):
        url = "/api/horarios-atendimento/"
        data = {
            "dia_da_semana": "segunda feira",
            "inicio": "14:00:00",
            "fim": "12:00:00",
            "profissional_fk": self.profissional.id,  
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
    
    def test_erro_create_paciente_sem_nome(self):
        url = "/api/paciente/"
        data = {
            "sobrenome": "Mendoça Inacio",
            "cpf": "06733563100",
            "rg": "12997",
            "orgao_expeditor": "SSP-GO",
            "sexo": "F",
            "celular": "62983107172",
            "email": "ana.julias@hotmail.com",
            "nascimento": "2006-02-20",
            "endereco_fk": self.endereco.id,   
            "convenio_fk": self.convenio.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_erro_create_paciente_cpf_invalido(self):
        url = "/api/paciente/"
        data = {
            "nome": "Ana Julia",
            "sobrenome": "Mendoça Inacio",
            "cpf": "098765432112",
            "rg": "12997",
            "orgao_expeditor": "SSP-GO",
            "sexo": "F",
            "celular": "62983107172",
            "email": "ana.julias@hotmail.com",
            "nascimento": "2006-02-20",
            "endereco_fk": self.endereco.id,   
            "convenio_fk": self.convenio.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_erro_create_paciente_sexo_invalido(self):
        url = "/api/paciente/"
        data = {
            "nome": "Ana Julia",
            "sobrenome": "Mendoça Inacio",
            "cpf": "06733563100",
            "rg": "12997",
            "orgao_expeditor": "SSP-GO",
            "sexo": "Mulher",
            "celular": "62983107172",
            "email": "ana.julias@hotmail.com",
            "nascimento": "2006-02-20",
            "endereco_fk": self.endereco.id,   
            "convenio_fk": self.convenio.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_erro_create_paciente_cpf_ja_existente(self):
        url = "/api/paciente/"
        data = {
            "nome": "Ana Julia",
            "sobrenome": "Mendoça Inacio",
            "cpf": "92708765191",
            "rg": "12997",
            "orgao_expeditor": "SSP-GO",
            "sexo": "F",
            "celular": "62983107172",
            "email": "ana.julias@hotmail.com",
            "nascimento": "2006-02-20",
            "endereco_fk": self.endereco.id,   
            "convenio_fk": self.convenio.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_erro_create_paciente_celular_incorreto(self):
        url = "/api/paciente/"
        data = {
            "nome": "Ana Julia",
            "sobrenome": "Mendoça Inacio",
            "cpf": "06733563100",
            "rg": "12997",
            "orgao_expeditor": "SSP-GO",
            "sexo": "F",
            "celular": "6298310717",
            "email": "ana.julias@hotmail.com",
            "nascimento": "2006-02-20",
            "endereco_fk": self.endereco.id,   
            "convenio_fk": self.convenio.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_erro_create_paciente_data_nascimento_formato_incorreto(self):
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
            "nascimento": "20-02-2006",
            "endereco_fk": self.endereco.id,   
            "convenio_fk": self.convenio.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    # Fluxo de updates 
    def test_update_convenio(self):
        url = f"/api/convenio/{self.convenio.id}/"
        data = {
            "nome": "Real Liberty SA",
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)
 
    def test_update_endereco(self):
        url = f"/api/endereco/{self.endereco.id}/"
        data = {
            "numero": 90
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_update_profissional(self):
        url = f"/api/profissional/{self.profissional.id}/"
        data = {
            "nome": "Jose Roberto",
            "sobrenome": "Mendonça Inacio",
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_update_procedimento(self):
        url = f"/api/procedimento/{self.procedimento.id}/"
        data = {
            "nome": "Cirurgia de Hemorroida com Enzimas Foliformes"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_update_solicitacao_agendamento(self):
        url = f"/api/solicitacoes-agendamento/{self.procedimento.id}/"
        data = {
            "data_consulta": "2024-11-23",
            "hora_inicio_consulta": "15:30:00",
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_update_profissional_procedimento(self):
        url = f"/api/profissional-procedimento/{self.profissional_procedimento.id}/"
        data = {
            "tempo_duracao": "00:45:00",
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_update_horario_atendimento(self):
        url = f"/api/horarios-atendimento/{self.horarios_atendimento.id}/"
        data = {
            "dia_da_semana": "2a",
            "inicio": "14:00:00",
            "fim": "20:00:00",
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_update_paciente(self):
        url = f"/api/paciente/{self.paciente.id}/"
        data = {
            "email": "jujubinha@gmail.com"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)
    