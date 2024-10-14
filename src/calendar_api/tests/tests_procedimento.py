from django.test import TestCase
from ..models import Procedimento
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class ProcedimentoTests(APITestCase):
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

        # Criação de um procedimento para testes
        self.procedimento = Procedimento.objects.create(
            nome="Procedimento Teste"
        )

    def test_create_procedimento_with_no_permission(self):
        """
        Teste falho: Usuário padrão tentando criar um procedimento sem permissão.
        """
        url = "/api/procedimento/"
        data = {
            "nome": "Novo Procedimento"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_list_procedimentos_with_no_permission(self):
        """
        Teste falho: Usuário padrão tentando listar procedimentos sem permissão.
        """
        url = "/api/procedimento/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_retrieve_procedimento_with_no_permission(self):
        """
        Teste falho: Usuário padrão tentando acessar um procedimento sem permissão.
        """
        url = "/api/procedimento/{}/".format(self.procedimento.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_update_procedimento_with_no_permission(self):
        """
        Teste falho: Usuário padrão tentando atualizar um procedimento sem permissão.
        """
        url = "/api/procedimento/{}/".format(self.procedimento.id)
        data = {
            "nome": "Procedimento Atualizado"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_partial_update_procedimento_with_no_permission(self):
        """
        Teste falho: Usuário padrão tentando atualizar parcialmente um procedimento.
        """
        url = "/api/procedimento/{}/".format(self.procedimento.id)
        data = {
            "nome": "Procedimento Parcialmente Atualizado"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_create_procedimento_with_permission(self):
        """
        Teste de sucesso: Usuário com permissão cria um procedimento.
        """
        # Autentica como staff
        self.client.force_authenticate(user=self.staff)

        url = "/api/procedimento/"
        data = {
            "nome": "Novo Procedimento"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)  # 201 Created

        # Verifica se o procedimento foi criado
        query = Procedimento.objects.filter(nome="Novo Procedimento")
        self.assertNotEqual(query.count(), 0)  # O procedimento deve ter sido criado

    def test_list_procedimentos_with_permission(self):
        """
        Teste de sucesso: Usuário com permissão lista procedimentos.
        """
        # Autentica como staff
        self.client.force_authenticate(user=self.staff)

        url = "/api/procedimento/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # 200 OK

    def test_retrieve_procedimento_with_permission(self):
        """
        Teste de sucesso: Usuário com permissão acessa um procedimento.
        """
        # Autentica como staff
        self.client.force_authenticate(user=self.staff)

        url = "/api/procedimento/{}/".format(self.procedimento.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # 200 OK

    def test_update_procedimento_with_permission(self):
        """
        Teste de sucesso: Usuário com permissão atualiza um procedimento.
        """
        # Autentica como staff
        self.client.force_authenticate(user=self.staff)

        url = "/api/procedimento/{}/".format(self.procedimento.id)
        data = {
            "nome": "Procedimento Atualizado"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)  # 200 OK

        # Verifica se o procedimento foi atualizado
        self.procedimento.refresh_from_db()
        self.assertEqual(self.procedimento.nome, "Procedimento Atualizado")

    def test_partial_update_procedimento_with_permission(self):
        """
        Teste de sucesso: Usuário com permissão atualiza parcialmente um procedimento.
        """
        # Autentica como staff
        self.client.force_authenticate(user=self.staff)

        url = "/api/procedimento/{}/".format(self.procedimento.id)
        data = {
            "nome": "Procedimento Parcialmente Atualizado"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)  # 200 OK

        # Verifica se o procedimento foi parcialmente atualizado
        self.procedimento.refresh_from_db()
        self.assertEqual(self.procedimento.nome, "Procedimento Parcialmente Atualizado")

    def test_create_procedimento_with_empty_name(self):
        """
        Teste falho: Usuário com permissão tenta criar um procedimento com nome vazio.
        """
        # Autentica como staff
        self.client.force_authenticate(user=self.staff)

        url = "/api/procedimento/"
        data = {
            "nome": "",  # Nome em branco
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)  # Nome em branco não é permitido
