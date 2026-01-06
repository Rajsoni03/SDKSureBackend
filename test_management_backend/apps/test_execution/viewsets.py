from rest_framework import permissions, viewsets

from .filters import TestRunFilter
from .models import TestRun
from .permissions import IsTestRunner
from .serializers import TestRunSerializer, TestScenarioSerializer
from .models import TestRun, TestScenario


class TestScenarioViewSet(viewsets.ModelViewSet):
    serializer_class = TestScenarioSerializer
    permission_classes = [permissions.IsAuthenticated, IsTestRunner]
    queryset = TestScenario.objects.prefetch_related("test_cases", "labels").select_related("created_by", "updated_by")
    search_fields = ["name", "description", "test_cases__title"]
    ordering_fields = ["name", "created_at", "updated_at"]


class TestRunViewSet(viewsets.ModelViewSet):
    """Manage test run lifecycle."""

    serializer_class = TestRunSerializer
    permission_classes = [permissions.IsAuthenticated, IsTestRunner]
    queryset = (
        TestRun.objects.prefetch_related("scenarios", "labels", "results")
        .select_related("created_by", "updated_by")
        .order_by("-created_at")
    )
    filterset_class = TestRunFilter
    search_fields = ["name", "description"]
    ordering_fields = ["created_at", "updated_at", "name"]
