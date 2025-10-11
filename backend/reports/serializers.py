from rest_framework import serializers

from .models import WeeklyReport


class WeeklyReportSerializer(serializers.ModelSerializer):
    professional = serializers.UUIDField(read_only=True)
    patient = serializers.UUIDField(read_only=True)

    class Meta:
        model = WeeklyReport
        fields = ["id", "professional", "patient", "week_start", "report_url", "generated_at"]
        read_only_fields = ["id", "professional", "patient", "week_start", "generated_at"]
