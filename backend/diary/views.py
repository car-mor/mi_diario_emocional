from collections import Counter

from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .ml_service import (
    analizar_emociones_texto,
    lematizar_texto,  # <-- IMPORTACIÓN AÑADIDA
    nlp,
    preprocesar_texto,  # <-- IMPORTACIÓN AÑADIDA
)
from .models import DiaryEntry
from .permissions import IsPatient
from .serializers import DiaryEntrySerializer

STOP_WORDS = nlp.Defaults.stop_words if nlp else set()


class DiaryEntryViewSet(viewsets.ModelViewSet):
    """
    ViewSet para que un PACIENTE gestione sus propias entradas del diario.
    """

    serializer_class = DiaryEntrySerializer
    permission_classes = [IsAuthenticated, IsPatient]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return DiaryEntry.objects.all().order_by("-entry_date")

        # Como el permiso IsPatient ya nos asegura que el usuario tiene este rol,
        # la lógica se simplifica.
        if hasattr(user, "patient_profile"):
            return DiaryEntry.objects.filter(patient=user.patient_profile).order_by("-entry_date")

        # Si por alguna razón es un paciente sin perfil, no devuelve nada.
        return DiaryEntry.objects.none()

    def perform_create(self, serializer):
        patient_profile = self.request.user.patient_profile
        today = timezone.now().date()

        if patient_profile.last_entry_date:
            days_diff = (today - patient_profile.last_entry_date).days
            if days_diff == 1:
                # El usuario escribió ayer, ¡la racha continúa!
                patient_profile.current_streak += 1
            elif days_diff > 1:
                # El usuario rompió la racha, se resetea a 1
                patient_profile.current_streak = 1
            # Si days_diff == 0, ya escribió hoy, no hacemos nada.
        else:
            # Es la primera entrada de su vida
            patient_profile.current_streak = 1

        # Actualizamos la fecha de la última entrada y guardamos
        patient_profile.last_entry_date = today
        # ----------------------------------------

        if not patient_profile.first_entry_date:
            patient_profile.first_entry_date = today

        patient_profile.save()
        content = serializer.validated_data.get("content", "")
        emociones_analizadas = analizar_emociones_texto(content)

        serializer.save(patient=patient_profile, analyzed_emotions=emociones_analizadas)

    @action(detail=False, methods=["get"], url_path="emotion-combinations")
    def emotion_combinations(self, request):
        """
        Calcula las 5 combinaciones de emociones más frecuentes PARA EL PACIENTE LOGUEADO.
        """
        user_entries = self.get_queryset()  # Ya está filtrado para este paciente
        combination_counts = Counter()
        for entry in user_entries:
            if len(entry.analyzed_emotions) > 1:
                combination_counts[tuple(sorted(entry.analyzed_emotions))] += 1
        most_common = [[" - ".join(comb), count] for comb, count in combination_counts.most_common(5)]
        return Response(most_common)

    @action(detail=False, methods=["get"], url_path="word-frequency")
    def word_frequency(self, request):
        """
        Calcula las 50 palabras más frecuentes PARA EL PACIENTE LOGUEADO.
        """
        user_entries = self.get_queryset()
        full_text = " ".join([entry.content for entry in user_entries])
        if not full_text.strip():
            return Response([])

        lemmas = lematizar_texto(preprocesar_texto(full_text))
        important_words = [lem for lem in lemmas if lem not in STOP_WORDS and lem.isalpha() and len(lem) > 2]
        word_counts = Counter(important_words)
        return Response(word_counts.most_common(50))
