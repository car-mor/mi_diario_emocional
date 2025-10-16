from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import DiaryEntry
from .permissions import IsPatient, IsProfessional  # Importa los permisos personalizados
from .serializers import DiaryEntrySerializer


class DiaryEntryViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    ViewSet para manejar las entradas del diario.
    Permite a los pacientes crear, ver, actualizar y eliminar sus propias entradas.
    Permite a los profesionales ver las entradas de sus pacientes asignados.
    """

    serializer_class = DiaryEntrySerializer
    permission_classes = [IsAuthenticated, IsPatient]

    def get_queryset(self):
        user = self.request.user

        # 1. PERMISO PARA SUPERUSUARIO (Admin ve todo)
        if user.is_superuser:
            return DiaryEntry.objects.all()

        # 2. FILTRADO BASADO EN ROL (Usuarios normales)
        if user.role == "patient":
            # Verifica si el perfil existe antes de acceder a él
            if hasattr(user, "patient_profile"):
                return DiaryEntry.objects.filter(patient=user.patient_profile)
            else:
                # Si es un paciente sin perfil (debería ser raro), no ve nada
                return DiaryEntry.objects.none()

        elif user.role == "professional":
            # Verifica si el perfil existe antes de acceder a él
            if hasattr(user, "professional_profile"):
                patients_of_professional = user.professional_profile.patients.all()
                return DiaryEntry.objects.filter(patient__in=patients_of_professional)
            else:
                # Si es un profesional sin perfil (el caso del Superusuario que falló), no ve nada
                return DiaryEntry.objects.none()

        return DiaryEntry.objects.none()  # Usuario autenticado sin rol definido

    def perform_create(self, serializer):
        """
        Sobrescribe este método para asociar la entrada del diario con el paciente
        que está autenticado automáticamente.
        """
        serializer.save(patient=self.request.user.patient_profile)

    # Nota: También se puede usar `permission_classes = [IsAuthenticated, IsPatient | IsProfessional]`
    # para controlar el acceso más detallado si es necesario.
    # En este caso, `get_queryset` ya se encarga del filtrado de datos.
