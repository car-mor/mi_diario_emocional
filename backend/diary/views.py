from collections import Counter

from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# --- 1. IMPORTACIÓN LIMPIA ---
# ¡Ahora importamos las dos funciones de nuestro ml_service!
from .ml_service import (
    analizar_emociones_con_beto,
    obtener_frecuencia_palabras,  # <-- Nueva importación
)
from .models import DiaryEntry
from .permissions import IsPatient
from .serializers import DiaryEntrySerializer

# --- 2. ELIMINADO ---
# Ya no necesitamos get_stop_words() ni STOP_WORDS aquí.
# Borra esas funciones y la variable global.
# def get_stop_words(): ...
# STOP_WORDS = get_stop_words()


class DiaryEntryViewSet(viewsets.ModelViewSet):
    """
    ViewSet para que un PACIENTE gestione sus propias entradas del diario.
    """

    serializer_class = DiaryEntrySerializer
    permission_classes = [IsAuthenticated, IsPatient]

    def get_queryset(self):
        # ... (esta función se queda exactamente igual)
        user = self.request.user
        if user.is_superuser:
            return DiaryEntry.objects.all().order_by("-entry_date")
        if hasattr(user, "patient_profile"):
            return DiaryEntry.objects.filter(patient=user.patient_profile).order_by("-entry_date")
        return DiaryEntry.objects.none()

    def perform_create(self, serializer):
        patient_profile = self.request.user.patient_profile

        patient_profile.update_streak_on_new_entry()

        # Lógica de ML (mantener igual)
        content = serializer.validated_data.get("content", "")
        emociones_lista, scores_dict = analizar_emociones_con_beto(content)

        serializer.save(
            patient=patient_profile,
            analyzed_emotions=emociones_lista,
            analyzed_scores=scores_dict,
        )

    @action(detail=False, methods=["get"], url_path="emotion-combinations")
    def emotion_combinations(self, request):
        # ... (esta función se queda exactamente igual)
        user_entries = self.get_queryset()
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        if start_date and end_date:
            try:
                end_date_obj = timezone.datetime.strptime(end_date, "%Y-%m-%d").date()
                end_date_inclusive = end_date_obj + timezone.timedelta(days=1)
                user_entries = user_entries.filter(entry_date__gte=start_date, entry_date__lt=end_date_inclusive)
            except (ValueError, TypeError):
                pass
        combination_counts = Counter()
        for entry in user_entries:
            emotions = entry.analyzed_emotions
            if emotions and emotions != ["neutro"]:
                combination_counts[tuple(sorted(emotions))] += 1
        most_common = [[" - ".join(comb), count] for comb, count in combination_counts.most_common(5)]
        return Response(most_common)

    # --- 3. ACCIÓN ACTUALIZADA ---
    @action(detail=False, methods=["get"], url_path="word-frequency")
    def word_frequency(self, request):
        """
        Calcula las 50 palabras más frecuentes LLAMANDO A LA API DE HF.
        """
        user_entries = self.get_queryset()
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        if start_date and end_date:
            try:
                end_date_obj = timezone.datetime.strptime(end_date, "%Y-%m-%d").date()
                end_date_inclusive = end_date_obj + timezone.timedelta(days=1)
                user_entries = user_entries.filter(entry_date__gte=start_date, entry_date__lt=end_date_inclusive)
            except (ValueError, TypeError):
                pass

        full_text = " ".join([entry.content for entry in user_entries])
        if not full_text.strip():
            return Response([])

        # --- Lógica de ML (AHORA ES UNA SOLA LÍNEA) ---
        # Borramos todo el procesamiento local (lemmas, STOP_WORDS, Counter)
        # y solo llamamos a nuestra nueva función de servicio:
        word_counts_list = obtener_frecuencia_palabras(full_text)

        return Response(word_counts_list)  # Devuelve la lista directamente
