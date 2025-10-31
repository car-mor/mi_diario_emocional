from collections import Counter

from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .ml_service import (
    NLP,
    analizar_emociones_con_beto,
    lematizar_texto_para_lista,
    preprocesar_texto,
)
from .models import DiaryEntry
from .permissions import IsPatient
from .serializers import DiaryEntrySerializer

STOP_WORDS = NLP.Defaults.stop_words if NLP else set()


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
        # 1. Llama al nuevo modelo de BETO
        emociones_lista, scores_dict = analizar_emociones_con_beto(content)

        # 2. Guarda ambos resultados en el serializer
        serializer.save(
            patient=patient_profile,
            analyzed_emotions=emociones_lista,
            analyzed_scores=scores_dict,
        )

    @action(detail=False, methods=["get"], url_path="emotion-combinations")
    def emotion_combinations(self, request):
        """
        Calcula las 5 combinaciones de emociones más frecuentes PARA EL PACIENTE LOGUEADO.
        """
        user_entries = self.get_queryset()  # Ya está filtrado para este paciente

        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        if start_date and end_date:
            try:
                # Asegurarse de que el rango de fechas sea inclusivo
                end_date_obj = timezone.datetime.strptime(end_date, "%Y-%m-%d").date()
                end_date_inclusive = end_date_obj + timezone.timedelta(days=1)
                user_entries = user_entries.filter(entry_date__gte=start_date, entry_date__lt=end_date_inclusive)
            except (ValueError, TypeError):
                pass  # Ignorar fechas mal formadas
        combination_counts = Counter()
        for entry in user_entries:
            emotions = entry.analyzed_emotions

            # Solo cuenta si la lista no está vacía Y no es ['neutro']
            if emotions and emotions != ["neutro"]:
                combination_counts[tuple(sorted(emotions))] += 1

        most_common = [[" - ".join(comb), count] for comb, count in combination_counts.most_common(5)]
        return Response(most_common)

    @action(detail=False, methods=["get"], url_path="word-frequency")
    def word_frequency(self, request):
        """
        Calcula las 50 palabras más frecuentes PARA EL PACIENTE LOGUEADO.
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

        lemmas = lematizar_texto_para_lista(preprocesar_texto(full_text))
        important_words = [lem for lem in lemmas if lem not in STOP_WORDS and lem.isalpha() and len(lem) > 2]
        word_counts = Counter(important_words)
        return Response(word_counts.most_common(50))
