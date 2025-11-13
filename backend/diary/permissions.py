# diary/permissions.py

from rest_framework.permissions import BasePermission


class IsPatient(BasePermission):
    """
    Permiso personalizado para permitir el acceso solo a usuarios con el rol 'patient'.
    """

    def has_permission(self, request, view):
        # Primero, asegúrate de que el usuario esté autenticado.
        if not request.user or not request.user.is_authenticated:
            return False
        # Luego, verifica que su rol sea 'patient'.
        return request.user.role == "patient"


class IsProfessional(BasePermission):
    """
    Permiso personalizado para permitir el acceso solo a usuarios con el rol 'professional'.
    """

    def has_permission(self, request, view):
        # Primero, asegúrate de que el usuario esté autenticado.
        if not request.user or not request.user.is_authenticated:
            return False
        # Luego, verifica que su rol sea 'professional'.
        return request.user.role == "professional"
