# reports/admin.py
from django.contrib import admin

from .models import WeeklyReport


@admin.register(WeeklyReport)
class WeeklyReportAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista del panel
    list_display = ("week_start", "patient", "professional", "generated_at")

    # Campos para filtrar la lista
    list_filter = ("week_start", "professional")

    # Campos de solo lectura
    readonly_fields = ("generated_at", "report_url")

    # Ordenar por fecha de generación más reciente
    ordering = ("-generated_at",)
