import uuid

from django.db import models

from users.models import Patient, Professional


class WeeklyReport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    professional = models.ForeignKey(
        Professional, on_delete=models.CASCADE, related_name="weekly_reports"
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="weekly_reports")
    week_start = models.DateField()
    report_url = models.URLField()
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("professional", "patient", "week_start")

    def __str__(self):
        return f"Reporte de {self.patient.alias} ({self.week_start})"
