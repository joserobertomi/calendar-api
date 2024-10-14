
from rest_framework.test import APITestCase
from ..models import CustomUser
from rest_framework import status


class UserTests(APITestCase):

    def setUp(self):
        # Criação de um superusuário para os testes
        self.staff_user = CustomUser.objects.create_superuser(
            name='Jeff',
            email='staff@example.com',
            password='password123'
        )

        # Criação de um usuário padrão para testes
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            name='Test User',
            cpf='12345678909'  # Exemplo de CPF válido
        )

        # URL base do endpoint
        self.url = '/api/users/'

        # Forçar autenticação do superusuário
        self.client.force_authenticate(user=self.staff_user)

    def test_create_user_with_existing_email(self):
        # Testa a criação de um usuário com um e-mail já existente
        data = {
            'email': 'testuser@example.com',
            'password': 'newpassword',
            'name': 'New User',
            'cpf': '10987654321'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Deve falhar com 400
        self.assertIn('email', response.data)  # Verifica se a resposta contém erro para o campo email

    def test_create_user_with_invalid_data(self):
        # Testa a criação de um usuário com dados inválidos
        data = {
            'email': 'invalid_email',  # E-mail inválido
            'password': 'newpassword',
            'name': '',
            'cpf': '123'  # CPF inválido
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Deve falhar com 400

    def test_retrieve_non_existing_user(self):
        # Testa a recuperação de um usuário que não existe
        response = self.client.get('/api/users/999/')  # ID não existente
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # Deve falhar com 404

    def test_update_non_existing_user(self):
        # Testa a atualização de um usuário que não existe
        data = {
            'name': 'Updated Name',
        }
        response = self.client.patch('/api/users/999/', data, format='json')  # ID não existente
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # Deve falhar com 404

    def test_destroy_with_no_permission(self):
        # Testa a exclusão de um usuário que não existe
        response = self.client.delete(f'/api/users/{self.staff_user.id}/')  # ID existente
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)  # Deve falhar com 405

    def test_change_group_for_non_existing_user(self):
        # Testa a alteração de grupo de um usuário que não existe
        self.client.force_authenticate(user=self.user)  # Simula a autenticação do usuário
        response = self.client.post(f'/api/users/999/change_group/', data={'group': 'New Group'})  # ID não existente
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # Deve falhar com 404

    def test_change_group_successfully(self):
        # Testa a alteração de grupo de um usuário sem permissões
        other_user = CustomUser.objects.create_user(
            email='otheruser@example.com',
            password='otherpassword',
            name='Other User',
            cpf='98765432109'
        )
        response = self.client.post(f'/api/users/{other_user.id}/change_group/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Acesso negado sem permissão


    def test_create_user_with_missing_email(self):
        # Testa a criação de um usuário sem campos obrigatórios
        data = {
            'password': '',
            'name': '',
            'cpf': ''
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Deve falhar com 400
    
    def test_create_user_with_missing_fields(self):
        # Testa a criação de um usuário sem campos obrigatórios
        data = {
            'email': '',
            'password': '',
            'name': '',
            'cpf': ''
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Deve falhar com 400

    def test_partial_update_non_existing_user(self):
        # Testa a atualização parcial de um usuário que não existe
        data = {
            'email': 'updateduser@example.com',
        }
        response = self.client.patch("/api/users/999/")  # ID não existente
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # Deve falhar com 404

    def test_partial_update_user_with_invalid_data(self):
        # Testa a atualização parcial de um usuário com dados inválidos
        data = {
            'email': 'invalid_email',  # E-mail inválido
        }
        response = self.client.patch(f'/api/users/{self.user.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Deve falhar com 400

    def test_create_user_success(self):
        # Testa a criação de um novo usuário com dados válidos
        data = {
            'email': 'bb@example.com',
            'password': 'newpassword123',
            'name': 'New User',
            'cpf': '04190689106'
        }
        response = self.client.post("/api/users/", data, format='json')
        print(response.data)  # Adicione esta linha para depuração
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Deve retornar 201
        self.assertEqual(CustomUser.objects.count(), 3)  # Verifica se um novo usuário foi criado

    def test_retrieve_existing_user(self):
        # Testa a recuperação de um usuário que existe
        response = self.client.get(f'/api/users/{self.user.id}/')  # ID existente
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Deve retornar 200
        self.assertEqual(response.data['email'], self.user.email)  # Verifica se o e-mail está correto

    def test_update_user_success(self):
        # Testa a atualização de um usuário existente com dados válidos
        data = {
            'name': 'Updated User',
        }
        response = self.client.patch(f'/api/users/{self.user.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Deve retornar 200
        self.user.refresh_from_db()  # Atualiza o usuário a partir do banco de dados
        self.assertEqual(self.user.name, 'Updated User')  # Verifica se o nome foi atualizado

    def test_change_group_success(self):
        # Forçar autenticação do superusuário para ter permissão para alterar grupos
        self.client.force_authenticate(user=self.staff_user)
        # Realiza a requisição para alterar o grupo do usuário
        response = self.client.post(f"/api/users/{self.user.id}/change_group/")
        # Verifica se a resposta é 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Deve retornar 200
        # Atualiza o usuário a partir do banco de dados
        self.user.refresh_from_db()  
        # Verifica se o usuário agora pertence ao novo grupo
        self.assertTrue(self.user.groups.filter(name='Profissional').exists())  # Verifica se o grupo foi alterado
