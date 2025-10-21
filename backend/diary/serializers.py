from rest_framework import serializers

from .models import DiaryEntry


class DiaryEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = DiaryEntry
        fields = [
            "id",
            "patient",
            "title",
            "entry_date",
            "content",
            "selected_emotions",  # Las que el usuario selecciona
            "analyzed_emotions",
            "content_length",
        ]
        # Hacemos los campos generados por el backend de solo lectura
        read_only_fields = [
            "id",
            "patient",
            "entry_date",
            "content_length",
            "analyzed_emotions",  # <-- AÑADIDO
        ]
