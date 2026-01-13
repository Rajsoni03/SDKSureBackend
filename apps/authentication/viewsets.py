from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view

from .permissions import IsAdmin
from .serializers import UserSerializer

User = get_user_model()


@extend_schema_view(
    list=extend_schema(tags=["Authentication"]),
    retrieve=extend_schema(tags=["Authentication"]),
    create=extend_schema(tags=["Authentication"]),
    update=extend_schema(tags=["Authentication"]),
    partial_update=extend_schema(tags=["Authentication"]),
    destroy=extend_schema(tags=["Authentication"]),
)
class UserViewSet(viewsets.ModelViewSet):
    """User management endpoints."""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    queryset = User.objects.all().order_by("-date_joined")
