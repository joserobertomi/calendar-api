from rest_framework.permissions import BasePermission

class IsAdminOnly(BasePermission):
    """
    Permissão personalizada que permite apenas usuários administradores acessar a view.
    """
    
    def has_permission(self, request, view):
        # Verifica se o usuário está autenticado e é um superusuário (admin)
        return request.user and request.user.is_authenticated and request.user.is_admin