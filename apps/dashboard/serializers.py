from rest_framework import serializers

from .models import DashboardMetric


class DashboardMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardMetric
        fields = ["id", "key", "value", "refreshed_at"]
        read_only_fields = ["id", "refreshed_at"]

