from django.test import TestCase

from calendar_api.calendar_models.user import CustomUser
from ..models import Prontuario, Paciente, Profissional, Convenio
from rest_framework.test import APITestCase


class ProntuarioTests(APITestCase):
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

        # Criação de um profissional para testes
        self.profissional = Profissional.objects.create(
            nome="Profissional Teste",
            sobrenome="Teste",
            cpf='12345678901',
            uf_registro='SP',
            n_registro=123456,
            tipo_registro='CRM',
            email='profissional@example.com'
        )

        # Criação de um paciente para testes
        self.paciente = Paciente.objects.create(
            nome="Paciente Teste",
            sobrenome="Teste",
            cpf='12345678902',
            rg='123456789',
            orgao_expeditor='SSP',
            sexo='M',
            celular='11987654321',
            email='paciente@example.com',
            nascimento='1990-01-01'
        )

        # Criação de um prontuário para testes
        self.prontuario = Prontuario.objects.create(
            texto="Texto do prontuário",
            profissional_fk=self.profissional,
            paciente_fk=self.paciente
        )

    def test_create_prontuario_with_no_permission(self):
        """
        Teste falho: Usuário padrão tentando criar um prontuário sem permissão.
        """
        url = "/api/prontuario/"
        data = {
            "texto": "Novo prontuário",
            "profissional_fk": self.profissional.id,
            "paciente_fk": self.paciente.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_list_prontuarios_with_no_permissions(self):
        """
        Teste falho: Usuário padrão tentando listar prontuários sem permissão.
        """
        url = "/api/prontuario/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_retrieve_prontuario_with_no_permissions(self):
        """
        Teste falho: Usuário padrão tentando acessar um prontuário sem permissão.
        """
        url = "/api/prontuario/{}/".format(self.prontuario.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_update_prontuario_with_no_permission(self):
        """
        Teste falho: Usuário padrão tentando atualizar um prontuário sem permissão.
        """
        url = "/api/prontuario/{}/".format(self.prontuario.id)
        data = {
            "texto": "Prontuário atualizado"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_partial_update_prontuario_with_no_permission(self):
        """
        Teste falho: Usuário padrão tentando atualizar parcialmente um prontuário.
        """
        url = "/api/prontuario/{}/".format(self.prontuario.id)
        data = {
            "texto": "Prontuário parcialmente atualizado"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_create_prontuario_with_permission(self):
        """
        Teste de sucesso: Usuário com permissão cria um prontuário.
        """
        # Autentica como staff e muda o grupo do usuário
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)


        url = "/api/prontuario/"
        data = {
            "texto": "Novo prontuário",
            "profissional_fk": self.profissional.id,
            "paciente_fk": self.paciente.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)  # 201 Created

        # Verifica se o prontuário foi criado
        query = Prontuario.objects.filter(
            texto="Novo prontuário",
            profissional_fk=self.profissional,
            paciente_fk=self.paciente
        )
        self.assertNotEqual(query.count(), 0)  # O prontuário deve ter sido criado

    def test_list_prontuarios_with_permission(self):
        """
        Teste de sucesso: Usuário com permissão lista prontuários.
        """
       # Autentica como staff e muda o grupo do usuário
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)


        url = "/api/prontuario/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # 200 OK

    def test_retrieve_prontuario_with_permission(self):
        """
        Teste de sucesso: Usuário com permissão acessa um prontuário.
        """
        # Autentica como staff e muda o grupo do usuário
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)


        url = "/api/prontuario/{}/".format(self.prontuario.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # 200 OK


    def test_partial_update_prontuario_with_permission(self):
        """
        Teste de sucesso: Usuário com permissão atualiza parcialmente um prontuário.
        """
       # Autentica como staff e muda o grupo do usuário
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)


        url = "/api/prontuario/{}/".format(self.prontuario.id)
        data = {
            "texto": "Prontuário parcialmente atualizado"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)  # 200 OK

        # Verifica se o prontuário foi parcialmente atualizado
        self.prontuario.refresh_from_db()
        self.assertEqual(self.prontuario.texto, "Prontuário parcialmente atualizado")

    def test_create_prontuario_with_empty_text(self):
        """
        Teste falho: Usuário com permissão tenta criar um prontuário com texto vazio.
        """
        # Autentica como staff e muda o grupo do usuário
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)


        url = "/api/prontuario/"
        data = {
            "texto": "",  # Texto em branco
            "profissional_fk": self.profissional.id,
            "paciente_fk": self.paciente.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)  # Texto em branco não é permitido
