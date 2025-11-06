import regex
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
            "analyzed_scores",
            "content_length",
        ]
        # Hacemos los campos generados por el backend de solo lectura
        read_only_fields = [
            "id",
            "patient",
            "entry_date",
            "content_length",
            "analyzed_emotions",
            "analyzed_scores",
        ]
    
    def validate_title(self, value):
        """
        Valida el título:
        - Requerido (no puede estar vacío o ser solo espacios).
        - Longitud entre 3 y 48 caracteres (contando emojis correctamente).
        - Permite cualquier caracter.
        """
        trimmed_value = value.strip()
        
        if not trimmed_value:
            raise serializers.ValidationError("El título es obligatorio.")
        
        # Usamos 'regex.findall(r'\X', ...)' para contar correctamente
        # los caracteres visibles (grapheme clusters), incluidos los emojis.
        char_length = len(regex.findall(r'\X', trimmed_value))
        
        if char_length < 3:
            raise serializers.ValidationError("El título debe tener al menos 3 caracteres.")
        
        if char_length > 48:
            raise serializers.ValidationError("El título no puede exceder los 48 caracteres.")
        
        # No hay más validaciones, se permiten todos los caracteres.
        return trimmed_value # Devolvemos el valor sin espacios al inicio/final
