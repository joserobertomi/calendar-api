from django.test import TestCase
from ..models import Convenio, CustomUser
from rest_framework.test import APITestCase


class ConvenioTests(APITestCase):
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

        # Criação de um convênio para testes
        self.convenio = Convenio.objects.create(
            nome="Convenio de Teste",
            inscricao="9876543210"
        )

    def test_create_convenio_with_no_permission(self):
        """
        Teste falho: Usuário padrão tentando criar um convênio sem permissão.
        """
        url = "/api/convenio/"
        data = {
            "nome": "Real Grandeza",
            "inscricao": "0123456789"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_list_convenios_with_no_permissions(self):
        """
        Teste falho: Usuário padrão tentando listar convênios sem permissão.
        """
        url = "/api/convenio/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)  # Sem permissão
        
    def test_retrieve_convenio_with_no_permissions(self):
        """
        Teste falho: Usuário padrão tentando acessar um convênio sem permissão.
        """
        url = "/api/convenio/{}/".format(self.convenio.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_update_convenio_with_no_permission(self):
        """
        Teste falho: Usuário padrão tentando atualizar um convênio sem permissão.
        """
        url = "/api/convenio/{}/".format(self.convenio.id)
        data = {
            "nome": "Convenio Atualizado",
            "inscricao": "1234567890"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_partial_update_convenio_with_no_permission(self):
        """
        Teste falho: Usuário padrão tentando atualizar parcialmente um convênio.
        """
        url = "/api/convenio/{}/".format(self.convenio.id)
        data = {
            "nome": "Convenio Parcialmente Atualizado"
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

    def test_create_convenio_with_permission(self):
        """
        Teste de sucesso: Usuário com permissão cria um convênio.
        """
        # Autentica como staff para mudar o grupo do usuário para profissional
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)

        url = "/api/convenio/"
        data = {
            "nome": "Real Grandeza",
            "inscricao": "0123456789"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)  # 201 Created

        # Verifica se o convênio foi criado
        query = Convenio.objects.filter(
            nome="Real Grandeza",
            inscricao="0123456789"
        )
        self.assertNotEqual(query.count(), 0)  # O convênio deve ter sido criado

    def test_list_convenios_with_permission(self):
        """
        Teste de sucesso: Usuário com permissão lista convênios.
        """
        # Autentica como staff e muda o grupo do usuário
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)

        url = "/api/convenio/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # 200 OK

    def test_retrieve_convenio_with_permission(self):
        """
        Teste de sucesso: Usuário com permissão acessa um convênio.
        """
        # Autentica como staff e muda o grupo do usuário
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)

        url = "/api/convenio/{}/".format(self.convenio.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # 200 OK

    def test_update_convenio_with_permission(self):
        """
        Teste de sucesso: Usuário com permissão atualiza um convênio.
        """
        # Autentica como staff e muda o grupo do usuário
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)

        url = "/api/convenio/{}/".format(self.convenio.id)
        data = {
            "nome": "Convenio Atualizado",
            "inscricao": "1234567890"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)  # 200 OK

        # Verifica se o convênio foi atualizado
        self.convenio.refresh_from_db()
        self.assertEqual(self.convenio.nome, "Convenio Atualizado")

    def test_partial_update_convenio_with_permission(self):
        """
        Teste de sucesso: Usuário com permissão atualiza parcialmente um convênio.
        """
        # Autentica como staff e muda o grupo do usuário
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)

        url = "/api/convenio/{}/".format(self.convenio.id)
        data = {
            "nome": "Convenio Parcialmente Atualizado"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)  # 200 OK

        # Verifica se o convênio foi parcialmente atualizado
        self.convenio.refresh_from_db()
        self.assertEqual(self.convenio.nome, "Convenio Parcialmente Atualizado")
        
    def test_create_convenio_with_empty_name(self):
       # Autentica como staff e muda o grupo do usuário
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)
        
        url = "/api/convenio/"
        data = {
            "nome": "",  # Nome em branco
            "inscricao": "0123456789"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)  # Nome em branco não é permitido

    def test_create_convenio_with_invalid_inscricao(self):
        # Autentica como staff e muda o grupo do usuário
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)
        
        url = "/api/convenio/"
        data = {
            "nome": "Convenio Válido",
            "inscricao": ""  # Inscrição em branco
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)  # Inscrição não pode estar em branco