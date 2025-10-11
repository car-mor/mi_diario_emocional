from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from diary.permissions import IsProfessional  # Reutilizamos el permiso

from .models import WeeklyReport
from .serializers import WeeklyReportSerializer


# Simulación de tarea asíncrona para generar reportes (con Celery, por ejemplo)
def generate_report_task(professional_id, patient_id, week_start):
    """
    Esta función simula una tarea en segundo plano.
    En un entorno real, usarías Celery para ejecutar esto.
    """
    print(f"Generando reporte para profesional {professional_id} y paciente {patient_id}...")
    # Lógica para generar el PDF (ej. con ReportLab o WeasyPrint)
    # y subirlo a un servicio de almacenamiento (ej. AWS S3)
    # Una vez completado, guarda la URL del reporte en el modelo WeeklyReport.

    WeeklyReport.objects.create(
        professional_id=professional_id,
        patient_id=patient_id,
        week_start=week_start,
        report_url="http://ejemplo.com/reportes/reporte_semanal.pdf",
    )


class WeeklyReportViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para que los profesionales puedan listar y ver reportes.
    Es de solo lectura porque los reportes se generan programáticamente, no vía API.
    """

    serializer_class = WeeklyReportSerializer
    permission_classes = [IsAuthenticated, IsProfessional]

    def get_queryset(self):
        user = self.request.user
        # Solo muestra los reportes del profesional que está logueado
        return WeeklyReport.objects.filter(professional=user.professional_profile)

    @action(detail=False, methods=["post"], url_path="generate")
    def generate_report(self, request):
        """
        Permite a un profesional generar un reporte semanal para uno de sus pacientes.
        """
        patient_id = request.data.get("patient_id")
        week_start = request.data.get("week_start")

        # Aquí validarías que el profesional está enlazado a ese paciente
        # y que la semana de inicio es válida.

        # Inicia la tarea de generación del reporte en segundo plano
        generate_report_task(self.request.user.professional_profile.pk, patient_id, week_start)

        return Response(
            {"message": "La generación del reporte ha sido iniciada. Serás notificado cuando esté listo."},
            status=status.HTTP_202_ACCEPTED,
        )
