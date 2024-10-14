from django.test import TestCase
from ..models import ProfissionalProcedimento
from ..models import Profissional
from ..models import Procedimento
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class ProfissionalProcedimentoTests(APITestCase):
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

        # Criação de profissionais e procedimentos para associar
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
            nome="Procedimento Teste"
        )

        # Criação de um profissional procedimento para testes
        self.profissional_procedimento = ProfissionalProcedimento.objects.create(
            profissional_fk=self.profissional,
            procedimento_fk=self.procedimento,
            tempo_duracao="00:30:00"  # 30 minutos
        )

    def test_create_profissional_procedimento_with_no_permission(self):
        """
        Teste falho: Usuário padrão tentando criar um profissional procedimento sem permissão.
        """
        url = "/api/profissional-procedimento/"
        data = {
            "profissional_fk": self.profissional.id,
            "procedimento_fk": self.procedimento.id,
            "tempo_duracao": "00:30:00"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_list_profissional_procedimento_with_no_permission(self):
        """
        Teste falho: Usuário padrão tentando listar profissional procedimentos sem permissão.
        """
        url = "/api/profissional-procedimento/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_retrieve_profissional_procedimento_with_no_permission(self):
        """
        Teste falho: Usuário padrão tentando acessar um profissional procedimento sem permissão.
        """
        url = "/api/profissional-procedimento/{}/".format(self.profissional_procedimento.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_update_profissional_procedimento_with_no_permission(self):
        """
        Teste falho: Usuário padrão tentando atualizar um profissional procedimento sem permissão.
        """
        url = "/api/profissional-procedimento/{}/".format(self.profissional_procedimento.id)
        data = {
            "tempo_duracao": "01:00:00"  # Atualiza para 1 hora
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_partial_update_profissional_procedimento_with_no_permission(self):
        """
        Teste falho: Usuário padrão tentando atualizar parcialmente um profissional procedimento.
        """
        url = "/api/profissional-procedimento/{}/".format(self.profissional_procedimento.id)
        data = {
            "tempo_duracao": "00:45:00"  # Atualiza para 45 minutos
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_create_profissional_procedimento_with_permission(self):
        """
        Teste de sucesso: Usuário com permissão cria um profissional procedimento.
        """
        # Autentica como staff e muda o grupo do usuário
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)

        url = "/api/profissional-procedimento/"
        data = {
            "profissional_fk": self.profissional.id,
            "procedimento_fk": self.procedimento.id,
            "tempo_duracao": "00:30:00"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)  # 201 Created

        # Verifica se o profissional procedimento foi criado
        query = ProfissionalProcedimento.objects.filter(profissional_fk=self.profissional)
        self.assertNotEqual(query.count(), 0)  # O profissional procedimento deve ter sido criado

    def test_list_profissional_procedimento_with_permission(self):
        """
        Teste de sucesso: Usuário com permissão lista profissional procedimentos.
        """
      # Autentica como staff e muda o grupo do usuário
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)

        url = "/api/profissional-procedimento/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # 200 OK

    def test_retrieve_profissional_procedimento_with_permission(self):
        """
        Teste de sucesso: Usuário com permissão acessa um profissional procedimento.
        """
        # Autentica como staff e muda o grupo do usuário
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)
        
        url = "/api/profissional-procedimento/{}/".format(self.profissional_procedimento.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # 200 OK

    def test_update_profissional_procedimento_with_permission(self):
        """
        Teste de sucesso: Usuário com permissão atualiza um profissional procedimento.
        """
        # Autentica como staff e muda o grupo do usuário
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)
        
        url = "/api/profissional-procedimento/{}/".format(self.profissional_procedimento.id)
        data = {
            "tempo_duracao": "01:00:00"  # Atualiza para 1 hora
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)  # 200 OK

        # Verifica se o profissional procedimento foi atualizado
        self.profissional_procedimento.refresh_from_db()
        self.assertEqual(str(self.profissional_procedimento.tempo_duracao), "1:00:00")  # Verifica a duração

    def test_partial_update_profissional_procedimento_with_permission(self):
        """
        Teste de sucesso: Usuário com permissão atualiza parcialmente um profissional procedimento.
        """
         # Autentica como staff e muda o grupo do usuário
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)
        

        url = "/api/profissional-procedimento/{}/".format(self.profissional_procedimento.id)
        data = {
            "tempo_duracao": "00:45:00"  # Atualiza para 45 minutos
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)  # 200 OK

        # Verifica se o profissional procedimento foi parcialmente atualizado
        self.profissional_procedimento.refresh_from_db()
        self.assertEqual(str(self.profissional_procedimento.tempo_duracao), "0:45:00")  # Verifica a duração
