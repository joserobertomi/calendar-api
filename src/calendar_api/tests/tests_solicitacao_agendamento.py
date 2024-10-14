from datetime import datetime
from django.test import TestCase
from ..models import SolicitacaoAgendamento, CustomUser, Profissional, Procedimento, Paciente
from rest_framework.test import APITestCase


class SolicitacaoAgendamentoTests(APITestCase):
    def setUp(self):
        # Criação de um usuário padrão para testes
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            name='Test User',
            cpf='12345678909'
        )
        # Criação de um superusuário (staff)
        self.staff = CustomUser.objects.create_superuser(
            email='admin@example.com',
            password='adminpassword',
            name='Admin User',
        )
        
        # Autentica o cliente como usuário padrão
        self.client.force_authenticate(user=self.user)

        # Criação de um profissional e um procedimento para testes
        self.profissional = Profissional.objects.create(
            nome="Profissional Teste",
            sobrenome="Teste",
            cpf="12345678901",
            uf_registro="SP",
            n_registro=123456,
            tipo_registro="tipo1",
            email="profissional@example.com"
        )
        
        self.procedimento = Procedimento.objects.create(
            nome='Procedimento Teste'
            # Adicione outros campos necessários aqui
        )
        self.paciente = Paciente.objects.create(
            nome='Paciente Teste',
            sobrenome='Sobrenome Teste',
            cpf='12345678909',
            rg='123456789',
            orgao_expeditor='SSP',
            sexo='M',
            celular='12345678901',
            email='paciente@example.com',
            nascimento='1990-01-01'
        )

        # Criação de uma solicitação de agendamento para testes
        self.solicitacao = SolicitacaoAgendamento.objects.create(
            data_consulta='2024-01-01',
            hora_inicio_consulta='10:00:00',
            profissional_fk=self.profissional,
            procedimento_fk=self.procedimento,
            paciente_fk=self.paciente
        )

    def test_create_solicitacao_agendamento_with_no_permission(self):
        """
        Teste falho: Usuário padrão tentando criar uma solicitação de agendamento sem permissão.
        """
        url = "/api/solicitacoes-agendamento/"
        data = {
            "data_consulta": "2024-01-02",
            "hora_inicio_consulta": "11:00:00",
            "profissional_fk": self.profissional.id,
            "procedimento_fk": self.procedimento.id,
            "paciente_fk": self.paciente.id
        }
        
        response = self.client.post(url, data, format='json')
        print(f"Response status: {response.status_code}, Content: {response.content}")  # Debug

        self.assertEqual(response.status_code, 403)  # Sem permissão


    def test_update_solicitacao_with_no_permission(self):
        """
        Teste falho: Usuário padrão tentando atualizar uma solicitação sem permissão.
        """
        url = f"/api/solicitacoes-agendamento/{self.solicitacao.id}/"
        data = {
            "data_consulta": "2024-01-02",
            "hora_inicio_consulta": "12:00:00"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_partial_update_solicitacao_with_no_permission(self):
        """
        Teste falho: Usuário padrão tentando atualizar parcialmente uma solicitação.
        """
        url = f"/api/solicitacoes-agendamento/{self.solicitacao.id}/"
        data = {
            "hora_inicio_consulta": "12:00:00"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_change_user_group_to_professional(self):
        """
        Teste de sucesso: Mudança de grupo de um usuário padrão para profissional.
        """
        # Autentica como staff
        self.client.force_authenticate(user=self.staff)
        
        url = f"/api/users/{self.user.id}/change_group/"
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, 200)  # Mudança de grupo com sucesso

        # Verifica se o grupo foi alterado
        self.user.refresh_from_db()
        self.assertIn("Profissional", [group.name for group in self.user.groups.all()])

    def test_create_solicitacao_agendamento_with_permission(self):
        """
        Teste de sucesso: Usuário com permissão cria uma solicitação de agendamento.
        """
        # Autentica como staff para mudar o grupo do usuário para profissional
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)

        url = "/api/solicitacoes-agendamento/"
        data = {
            "data_consulta": "2024-01-02",
            "hora_inicio_consulta": "11:00:00",
            "profissional_fk": self.profissional.id,
            "procedimento_fk": self.procedimento.id,
            "paciente_fk": self.paciente.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)  # 201 Created

        # Verifica se a solicitação foi criada
        query = SolicitacaoAgendamento.objects.filter(
            data_consulta="2024-01-02",
            hora_inicio_consulta="11:00:00",
            profissional_fk=self.profissional,
            procedimento_fk=self.procedimento,
            paciente_fk=self.paciente
        )
        self.assertNotEqual(query.count(), 0)  # A solicitação deve ter sido criada

    def test_list_solicitacoes_with_permission(self):
        """
        Teste de sucesso: Usuário com permissão lista solicitações.
        """
        # Autentica como staff e muda o grupo do usuário
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)

        url = "/api/solicitacoes-agendamento/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # 200 OK

    def test_retrieve_solicitacao_with_permission(self):
        """
        Teste de sucesso: Usuário com permissão acessa uma solicitação.
        """
        # Autentica como staff e muda o grupo do usuário
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)

        url = f"/api/solicitacoes-agendamento/{self.solicitacao.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # 200 OK

