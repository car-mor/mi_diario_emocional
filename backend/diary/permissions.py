from rest_framework import permissions


class IsPatient(permissions.BasePermission):
    """
    Permiso personalizado para permitir acceso solo a usuarios con el rol 'patient'.
    """

    def has_permission(self, request, view):
        return hasattr(request.user, "patient_profile")


class IsProfessional(permissions.BasePermission):
    """
    Permiso personalizado para permitir acceso solo a usuarios con el rol 'professional'.
    """

    def has_permission(self, request, view):
        return hasattr(request.user, "professional_profile")
