from rest_framework.permissions import BasePermission

class IsStaff(BasePermission):
    """
    Permissão customizada para garantir que o usuário seja staff (admin).
    """

    def has_permission(self, request, view):
        return request.user.is_staff

class IsOwnAccount(BasePermission):
    """
    Permissão que permite que o usuário acesse apenas sua própria conta.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user

class IsOnlyAllowedToChangeOwn(BasePermission):
    """
        Permissão personalizada que permite acessar apenas a permissao allowed to change own.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_superuser:
            return True
        
        if not user.has_perm("calendar_api.only_change_own"):
            return True
        
        if hasattr(obj, 'user') and obj.user == user:
            return True

        if obj.pk == user.pk:
            return True
            
        return False
