from django.test import TestCase
from ..models import Endereco, CustomUser
from rest_framework.test import APITestCase


class EnderecoTests(APITestCase):
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

        # Criação de um endereço para testes
        self.endereco = Endereco.objects.create(
            cep="12345678",
            rua="Rua de Teste",
            bairro="Bairro Teste",
            numero=123,
            cidade="Cidade Teste",
            estado="SP",
            complemento="Apto 101"
        )

    def test_create_endereco_with_no_permission(self):
        """
        Teste falho: Usuário padrão tentando criar um endereço sem permissão.
        """
        url = "/api/endereco/"
        data = {
            "cep": "87654321",
            "rua": "Rua Nova",
            "bairro": "Bairro Novo",
            "numero": 456,
            "cidade": "Cidade Nova",
            "estado": "RJ",
            "complemento": "Apto 202"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_list_enderecos_with_no_permissions(self):
        """
        Teste falho: Usuário padrão tentando listar endereços sem permissão.
        """
        url = "/api/endereco/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_retrieve_endereco_with_no_permissions(self):
        """
        Teste falho: Usuário padrão tentando acessar um endereço sem permissão.
        """
        url = "/api/endereco/{}/".format(self.endereco.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_update_endereco_with_no_permission(self):
        """
        Teste falho: Usuário padrão tentando atualizar um endereço sem permissão.
        """
        url = "/api/endereco/{}/".format(self.endereco.id)
        data = {
            "rua": "Rua Atualizada",
            "numero": 789
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_partial_update_endereco_with_no_permission(self):
        """
        Teste falho: Usuário padrão tentando atualizar parcialmente um endereço.
        """
        url = "/api/endereco/{}/".format(self.endereco.id)
        data = {
            "complemento": "Apto 303"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_create_endereco_with_permission(self):
        """
        Teste de sucesso: Usuário com permissão cria um endereço.
        """
        # Autentica como staff para mudar o grupo do usuário para profissional
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)

        url = "/api/endereco/"
        data = {
            "cep": "87654321",
            "rua": "Rua Nova",
            "bairro": "Bairro Novo",
            "numero": 456,
            "cidade": "Cidade Nova",
            "estado": "RJ",
            "complemento": "Apto 202"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)  # 201 Created

        # Verifica se o endereço foi criado
        query = Endereco.objects.filter(
            cep="87654321",
            rua="Rua Nova"
        )
        self.assertNotEqual(query.count(), 0)  # O endereço deve ter sido criado

    def test_list_enderecos_with_permission(self):
        """
        Teste de sucesso: Usuário com permissão lista endereços.
        """
        # Autentica como staff e muda o grupo do usuário
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)

        url = "/api/endereco/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # 200 OK

    def test_retrieve_endereco_with_permission(self):
        """
        Teste de sucesso: Usuário com permissão acessa um endereço.
        """
        # Autentica como staff e muda o grupo do usuário
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)

        url = "/api/endereco/{}/".format(self.endereco.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # 200 OK

    
    def test_create_endereco_with_invalid_cep(self):
        """
        Teste falho: Criação de endereço com CEP inválido.
        """
        # Autentica como staff e muda o grupo do usuário
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)

        url = "/api/endereco/"
        data = {
            "cep": "123",  # CEP inválido
            "rua": "Rua Nova",
            "bairro": "Bairro Novo",
            "numero": 456,
            "cidade": "Cidade Nova",
            "estado": "RJ",
            "complemento": "Apto 202"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)  # CEP inválido

    def test_create_endereco_with_empty_rua(self):
        """
        Teste falho: Criação de endereço com o campo 'rua' vazio.
        """
        # Autentica como staff e muda o grupo do usuário
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)

        url = "/api/endereco/"
        data = {
            "cep": "87654321",
            "rua": "",  # Rua em branco
            "bairro": "Bairro Novo",
            "numero": 456,
            "cidade": "Cidade Nova",
            "estado": "RJ",
            "complemento": "Apto 202"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)  # Rua em branco não é permitido
