# diary/admin.py
from django.contrib import admin

from .models import DiaryEntry


@admin.register(DiaryEntry)
class DiaryEntryAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista del panel
    list_display = ("title", "patient", "entry_date", "content_length")

    # Campos para filtrar la lista
    list_filter = ("entry_date", "patient__alias")

    # Campos para buscar
    search_fields = ("title", "content")

    # Campos de solo lectura que no se pueden editar en el formulario
    readonly_fields = ("entry_date", "content_length")
