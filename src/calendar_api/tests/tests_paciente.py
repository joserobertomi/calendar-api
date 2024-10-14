from django.test import TestCase
from ..models import Paciente, CustomUser, Endereco, Convenio
from rest_framework.test import APITestCase


class PacienteTests(APITestCase):
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

        # Criação de um endereço e convênio para associar ao paciente
        self.endereco = Endereco.objects.create(
            rua="Rua Teste",
            cidade="Cidade Teste",
            estado="SP",
            cep="12345678"
        )
        self.convenio = Convenio.objects.create(
            nome="Convenio Teste",
            inscricao="9876543210"
        )

        # Criação de um paciente para testes
        self.paciente = Paciente.objects.create(
            nome="Paciente",
            sobrenome="Teste",
            cpf="98765432109",
            rg="123456789",
            orgao_expeditor="SSP",
            sexo="M",
            celular="11987654321",
            email="paciente@example.com",
            nascimento="1990-01-01",
            endereco_fk=self.endereco,
            convenio_fk=self.convenio,
        )

    def test_create_paciente_with_no_permission(self):
        """
        Teste falho: Usuário padrão tentando criar um paciente sem permissão.
        """
        url = "/api/paciente/"
        data = {
            "nome": "Paciente",
            "sobrenome": "Novo",
            "cpf": "01234567890",
            "rg": "987654321",
            "orgao_expeditor": "SSP",
            "sexo": "F",
            "celular": "11987654322",
            "email": "novo@example.com",
            "nascimento": "1995-01-01",
            "endereco_fk": self.endereco.id,
            "convenio_fk": self.convenio.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_list_pacientes_with_no_permission(self):
        """
        Teste falho: Usuário padrão tentando listar pacientes sem permissão.
        """
        url = "/api/paciente/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)  # Sem permissão
        
    def test_retrieve_paciente_with_no_permission(self):
        """
        Teste falho: Usuário padrão tentando acessar um paciente sem permissão.
        """
        url = f"/api/paciente/{self.paciente.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_update_paciente_with_no_permission(self):
        """
        Teste falho: Usuário padrão tentando atualizar um paciente sem permissão.
        """
        url = f"/api/paciente/{self.paciente.id}/"
        data = {
            "nome": "Paciente Atualizado",
            "sobrenome": "Atualizado"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_partial_update_paciente_with_no_permission(self):
        """
        Teste falho: Usuário padrão tentando atualizar parcialmente um paciente.
        """
        url = f"/api/paciente/{self.paciente.id}/"
        data = {
            "nome": "Paciente Parcialmente Atualizado"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_create_paciente_with_permission(self):
        """
        Teste de sucesso: Usuário com permissão cria um paciente.
        """
        # Autentica como staff para mudar o grupo do usuário para profissional
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)

        url = "/api/paciente/"
        data = {
            "nome": "Paciente",
            "sobrenome": "Novo",
            "cpf": "01234567890",
            "rg": "987654321",
            "orgao_expeditor": "SSP",
            "sexo": "F",
            "celular": "11987654322",
            "email": "novo@example.com",
            "nascimento": "1995-01-01",
            "endereco_fk": self.endereco.id,
            "convenio_fk": self.convenio.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)  # 201 Created

        # Verifica se o paciente foi criado
        query = Paciente.objects.filter(
            nome="Paciente",
            sobrenome="Novo",
            cpf="01234567890"
        )
        self.assertNotEqual(query.count(), 0)  # O paciente deve ter sido criado

    def test_list_pacientes_with_permission(self):
        """
        Teste de sucesso: Usuário com permissão lista pacientes.
        """
        # Autentica como staff e muda o grupo do usuário
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)

        url = "/api/paciente/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # 200 OK

    def test_retrieve_paciente_with_permission(self):
        """
        Teste de sucesso: Usuário com permissão acessa um paciente.
        """
        # Autentica como staff e muda o grupo do usuário
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)

        url = f"/api/paciente/{self.paciente.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # 200 OK

    def test_update_paciente_with_permission(self):
        """
        Teste de sucesso: Usuário com permissão atualiza um paciente.
        """
        # Autentica como staff e muda o grupo do usuário
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)

        url = f"/api/paciente/{self.paciente.id}/"
        data = {
            "nome": "Paciente Atualizado",
            "sobrenome": "Atualizado"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)  # 200 OK

        # Verifica se o paciente foi atualizado
        self.paciente.refresh_from_db()
        self.assertEqual(self.paciente.nome, "Paciente Atualizado")

    def test_partial_update_paciente_with_permission(self):
        """
        Teste de sucesso: Usuário com permissão atualiza parcialmente um paciente.
        """
        # Autentica como staff e muda o grupo do usuário
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)

        url = f"/api/paciente/{self.paciente.id}/"
        data = {
            "nome": "Paciente Parcialmente Atualizado"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)  # 200 OK

        # Verifica se o paciente foi parcialmente atualizado
        self.paciente.refresh_from_db()
        self.assertEqual(self.paciente.nome, "Paciente Parcialmente Atualizado")

    def test_create_paciente_with_invalid_email(self):
        """
        Teste falho: Tentar criar um paciente com e-mail inválido.
        """
        # Autentica como staff e muda o grupo do usuário
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)
        
        url = "/api/paciente/"
        data = {
            "nome": "Paciente",
            "sobrenome": "Invalido",
            "cpf": "01234567890",
            "rg": "987654321",
            "orgao_expeditor": "SSP",
            "sexo": "F",
            "celular": "11987654322",
            "email": "email_invalido",  # Email inválido
            "nascimento": "1995-01-01",
            "endereco_fk": self.endereco.id,
            "convenio_fk": self.convenio.id,
        }
        response = self.client
