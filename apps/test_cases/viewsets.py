from rest_framework import permissions, viewsets

from .models import Label, TestCase, TestType
from .serializers import LabelSerializer, TestCaseSerializer, TestTypeSerializer


class TestCaseViewSet(viewsets.ModelViewSet):
    """CRUD endpoints for test cases."""

    serializer_class = TestCaseSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = TestCase.objects.all().order_by("title")
    search_fields = ["title", "description"]
    filterset_fields = ["test_type", "is_active"]
    ordering_fields = ["title", "created_at"]


class TestTypeViewSet(viewsets.ModelViewSet):
    serializer_class = TestTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = TestType.objects.all().order_by("name")


class LabelViewSet(viewsets.ModelViewSet):
    serializer_class = LabelSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Label.objects.all().order_by("name")
