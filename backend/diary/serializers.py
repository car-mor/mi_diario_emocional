from rest_framework import serializers

from .models import DiaryEntry


class DiaryEntrySerializer(serializers.ModelSerializer):
    # `read_only=True` asegura que el ID del paciente no se pueda modificar desde el frontend
    patient = serializers.UUIDField(read_only=True)

    class Meta:
        model = DiaryEntry
        fields = [
            "id",
            "patient",
            "title",
            "entry_date",
            "content",
            "selected_emotions",
            "emotion_summary",
        ]
        read_only_fields = ["id", "entry_date", "content_length"]
