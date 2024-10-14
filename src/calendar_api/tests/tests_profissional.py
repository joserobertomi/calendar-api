from django.test import TestCase
from ..models import Profissional, CustomUser
from rest_framework.test import APITestCase


class ProfissionalTests(APITestCase):
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
            nome="João",
            sobrenome="Silva",
            cpf="12345678909",
            uf_registro="SP",
            n_registro=12345,
            tipo_registro="CRM",
            email="joao.silva@example.com"
        )

    def test_create_profissional_with_no_permission(self):
        """
        Teste falho: Usuário padrão tentando criar um profissional sem permissão.
        """
        url = "/api/profissional/"
        data = {
            "nome": "Ana",
            "sobrenome": "Pereira",
            "cpf": "98765432100",
            "uf_registro": "RJ",
            "n_registro": 67890,
            "tipo_registro": "CRM",
            "email": "ana.pereira@example.com"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_list_profissionais_with_no_permissions(self):
        """
        Teste falho: Usuário padrão tentando listar profissionais sem permissão.
        """
        url = "/api/profissional/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_retrieve_profissional_with_no_permissions(self):
        """
        Teste falho: Usuário padrão tentando acessar um profissional sem permissão.
        """
        url = f"/api/profissional/{self.profissional.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_update_profissional_with_no_permission(self):
        """
        Teste falho: Usuário padrão tentando atualizar um profissional sem permissão.
        """
        url = f"/api/profissional/{self.profissional.id}/"
        data = {
            "nome": "João Atualizado",
            "sobrenome": "Silva Atualizado",
            "cpf": "12345678909",
            "uf_registro": "SP",
            "n_registro": 12345,
            "tipo_registro": "CRM",
            "email": "joao.silva.atualizado@example.com"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_partial_update_profissional_with_no_permission(self):
        """
        Teste falho: Usuário padrão tentando atualizar parcialmente um profissional.
        """
        url = f"/api/profissional/{self.profissional.id}/"
        data = {
            "nome": "João Parcialmente Atualizado"
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
