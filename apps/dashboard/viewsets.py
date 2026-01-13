from rest_framework import permissions, viewsets

from .models import DashboardMetric
from .serializers import DashboardMetricSerializer


class DashboardMetricViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only metrics for dashboards."""

    serializer_class = DashboardMetricSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = DashboardMetric.objects.all().order_by("key")

