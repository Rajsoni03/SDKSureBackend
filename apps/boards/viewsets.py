from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import BoardFilter
from .models import Board, BoardLog, Capability, PCStats, Relay, TestPC
from .serializers import (
    BoardLogSerializer,
    BoardSerializer,
    CapabilitySerializer,
    PCStatsSerializer,
    RelaySerializer,
    TestPCSerializer,
)


class CapabilityViewSet(viewsets.ModelViewSet):
    """CRUD operations for board capabilities."""

    serializer_class = CapabilitySerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Capability.objects.all().order_by("name")
    search_fields = ["name"]
    ordering_fields = ["name", "created_at", "updated_at"]


class RelayViewSet(viewsets.ModelViewSet):
    """CRUD operations for relays."""

    serializer_class = RelaySerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Relay.objects.all().order_by("relay_name")
    search_fields = ["relay_name", "ip_address", "mac_address"]
    ordering_fields = ["relay_name", "status", "created_at", "updated_at", "last_checked_at"]


class TestPCViewSet(viewsets.ModelViewSet):
    """CRUD operations for test PCs."""

    serializer_class = TestPCSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = TestPC.objects.all().order_by("hostname")
    search_fields = ["hostname", "ip_address", "domain_name"]
    ordering_fields = ["hostname", "status", "os_version", "created_at", "updated_at"]


class PCStatsViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only viewset for test PC performance stats."""

    serializer_class = PCStatsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = PCStats.objects.select_related("test_pc").all().order_by("-timestamp")
    search_fields = ["test_pc__hostname", "status"]
    ordering_fields = ["timestamp", "status", "cpu_percent", "memory_percent", "disk_percent"]


class BoardViewSet(viewsets.ModelViewSet):
    """CRUD operations for boards."""

    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = (
        Board.objects.select_related("test_pc", "relay")
        .prefetch_related("capabilities")
        .all()
        .order_by("name")
    )
    filterset_class = BoardFilter
    search_fields = ["name", "hardware_serial_number", "project", "platform", "test_farm", "board_ip"]
    ordering_fields = [
        "name",
        "hardware_serial_number",
        "project",
        "platform",
        "status",
        "test_farm",
        "created_at",
        "updated_at",
        "last_heartbeat_at",
    ]

    @action(detail=True, methods=["get"])
    def logs(self, request, pk=None):
        logs = BoardLog.objects.filter(board_id=pk).order_by("-created_at")[:50]
        data = BoardLogSerializer(logs, many=True).data
        return Response(data)
