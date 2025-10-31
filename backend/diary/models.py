import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone

from users.models import Patient


class DiaryEntry(models.Model):
    EMOTION_CHOICES = (
        ("alegria", "Alegría"),
        ("tristeza", "Tristeza"),
        ("ira", "Ira"),
        ("miedo", "Miedo"),
        ("asco", "Asco"),
        ("sorpresa", "Sorpresa"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="diary_entries")
    title = models.CharField(max_length=100, default="Sin título")
    entry_date = models.DateTimeField(default=timezone.now)
    content = models.TextField()

    # PERFECTO - NO CAMBIAR. Almacena la selección manual del usuario.
    selected_emotions = ArrayField(models.CharField(max_length=20, choices=EMOTION_CHOICES), default=list, blank=True)

    # NUEVO CAMPO - AÑADIR. Almacena el resultado del análisis del modelo.
    analyzed_emotions = ArrayField(models.CharField(max_length=20), default=list, blank=True)
    analyzed_scores = models.JSONField(default=dict, blank=True)
    content_length = models.IntegerField(editable=False)

    def save(self, *args, **kwargs):
        self.content_length = len(self.content)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient.alias} - {self.title}"
