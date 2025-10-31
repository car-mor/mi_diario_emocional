from rest_framework.permissions import BasePermission


class IsProfessional(BasePermission):
    """
    Permiso personalizado para permitir el acceso solo a usuarios
    con el rol 'professional'.
    """

    def has_permission(self, request, view):
        # 1. Primero, nos aseguramos de que el usuario esté autenticado.
        #    (Aunque ya usamos IsAuthenticated, es buena práctica ser explícitos).
        if not request.user or not request.user.is_authenticated:
            return False

        # 2. Verificamos que el rol del usuario sea 'professional'.
        #    Esto se basa en el campo 'role' de tu modelo User.
        return request.user.role == "professional"


class IsPatient(BasePermission):
    """
    Permiso personalizado para permitir el acceso solo a usuarios
    con el rol 'patient'.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        # Verificamos que el rol del usuario sea 'patient'.
        return request.user.role == "patient"
