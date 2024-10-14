from django.test import TestCase
from ..models import HorariosAtendimento
from ..models import Profissional
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class HorariosAtendimentoTests(APITestCase):
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

        # Criação de um profissional para associar aos horários de atendimento
        self.profissional = Profissional.objects.create(
            nome="Profissional Teste",
            sobrenome="Teste",
            cpf="12345678901",
            uf_registro="SP",
            n_registro=123456,
            tipo_registro="tipo1",
            email="profissional@example.com"
        )

        # Criação de horários de atendimento para testes
        self.horario = HorariosAtendimento.objects.create(
            dia_da_semana="Seg",  # Exemplo: 'Seg' para Segunda-feira
            inicio="09:00",
            fim="17:00",
            profissional_fk=self.profissional
        )

    def test_create_horarios_atendimento_with_no_permission(self):
        """
        Teste falho: Usuário padrão tentando criar um horário de atendimento sem permissão.
        """
        url = "/api/horarios-atendimento/"
        data = {
            "dia_da_semana": "Seg",
            "inicio": "09:00",
            "fim": "17:00",
            "profissional_fk": self.profissional.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_list_horarios_atendimento_with_no_permission(self):
        """
        Teste falho: Usuário padrão tentando listar horários de atendimento sem permissão.
        """
        url = "/api/horarios-atendimento/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_retrieve_horario_atendimento_with_no_permission(self):
        """
        Teste falho: Usuário padrão tentando acessar um horário de atendimento sem permissão.
        """
        url = "/api/horarios-atendimento/{}/".format(self.horario.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_update_horarios_atendimento_with_no_permission(self):
        """
        Teste falho: Usuário padrão tentando atualizar um horário de atendimento sem permissão.
        """
        url = "/api/horarios-atendimento/{}/".format(self.horario.id)
        data = {
            "dia_da_semana": "Ter",
            "inicio": "10:00",
            "fim": "18:00"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_partial_update_horarios_atendimento_with_no_permission(self):
        """
        Teste falho: Usuário padrão tentando atualizar parcialmente um horário de atendimento.
        """
        url = "/api/horarios-atendimento/{}/".format(self.horario.id)
        data = {
            "fim": "16:00"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 403)  # Sem permissão

    def test_create_horarios_atendimento_with_permission(self):
        """
        Teste de sucesso: Usuário com permissão cria um horário de atendimento.
        """
       # Autentica como staff e muda o grupo do usuário
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)

        url = "/api/horarios-atendimento/"
        data = {
            "dia_da_semana": "2a",
            "inicio": "09:00",
            "fim": "17:00",
            "profissional_fk": self.profissional.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)  # 201 Created

        # Verifica se o horário de atendimento foi criado
        query = HorariosAtendimento.objects.filter(dia_da_semana="Seg")
        self.assertNotEqual(query.count(), 0)  
        
    def test_list_horarios_atendimento_with_permission(self):
        """
        Teste de sucesso: Usuário com permissão lista horários de atendimento.
        """
        # Autentica como staff e muda o grupo do usuário
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)

        url = "/api/horarios-atendimento/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # 200 OK

    def test_retrieve_horario_atendimento_with_permission(self):
        """
        Teste de sucesso: Usuário com permissão acessa um horário de atendimento.
        """
     # Autentica como staff e muda o grupo do usuário
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)

        url = "/api/horarios-atendimento/{}/".format(self.horario.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # 200 OK

    def test_update_horarios_atendimento_with_permission(self):
        """
        Teste de sucesso: Usuário com permissão atualiza um horário de atendimento.
        """
       # Autentica como staff e muda o grupo do usuário
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)

        url = "/api/horarios-atendimento/{}/".format(self.horario.id)
        data = {
            "dia_da_semana": "3a",
            "inicio": "10:00",
            "fim": "18:00",
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_partial_update_horarios_atendimento_with_permission(self):
        """
        Teste de sucesso: Usuário com permissão atualiza parcialmente um horário de atendimento.
        """
       # Autentica como staff e muda o grupo do usuário
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)

        url = "/api/horarios-atendimento/{}/".format(self.horario.id)
        data = {
            "fim": "16:00"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)  # 200 OK

        # Verifica se o horário foi parcialmente atualizado
        self.horario.refresh_from_db()
        self.assertEqual(self.horario.fim.strftime("%H:%M"), "16:00")

    def test_create_horarios_atendimento_with_invalid_time(self):
        """
        Teste falho: Usuário com permissão tenta criar um horário de atendimento com hora de início posterior à hora de término.
        """
       # Autentica como staff e muda o grupo do usuário
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)

        url = "/api/horarios-atendimento/"
        data = {
            "dia_da_semana": "Seg",
            "inicio": "18:00",
            "fim": "09:00",
            "profissional_fk": self.profissional.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)  # 400 Bad Request

    def test_update_horarios_atendimento_with_invalid_time(self):
        """
        Teste falho: Usuário com permissão tenta atualizar um horário de atendimento com hora de início posterior à hora de término.
        """
        # Autentica como staff e muda o grupo do usuário
        self.client.force_authenticate(user=self.staff)
        self.client.post(f"/api/users/{self.user.id}/change_group/", format='json')
        self.client.force_authenticate(user=self.user)

        url = "/api/horarios-atendimento/{}/".format(self.horario.id)
        data = {
            "dia_da_semana": "3a",
            "inicio": "18:00",  # Hora de início posterior à hora de término
            "fim": "17:00"
        }
        response = self.client.put(url, data, format='json')
        
        # Verifique se a resposta é um 200
        self.assertEqual(response.status_code, 200)  