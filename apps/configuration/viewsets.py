from rest_framework import permissions, viewsets

from .models import SystemConfiguration
from .serializers import SystemConfigurationSerializer


class SystemConfigurationViewSet(viewsets.ModelViewSet):
    """Manage system configuration entries."""

    serializer_class = SystemConfigurationSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = SystemConfiguration.objects.all().order_by("key")

