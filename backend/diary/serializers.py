from rest_framework import serializers

from .models import DiaryEntry


class DiaryEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = DiaryEntry
        fields = [
            "id",
            "patient",  # <-- Lo mantenemos para lectura
            "title",
            "entry_date",
            "content",
            "selected_emotions",
            "emotion_summary",
            "content_length",  # <-- AÑADIDO
        ]
        # Hacemos que 'patient' sea de solo lectura para evitar que se envíe desde el frontend
        read_only_fields = ["id", "patient", "entry_date", "content_length"]
