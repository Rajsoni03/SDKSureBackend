from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import extend_schema, extend_schema_view
from .serializers import UserSerializer
from .permissions import IsAdmin, IsSuperAdmin
from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

@extend_schema(
    tags=["Authentication"],
    summary="Login to obtain access and refresh tokens",
)
class LoginView(TokenObtainPairView):
    """JWT login endpoint (email/username + password)."""


@extend_schema(
    tags=["Authentication"],
    summary="Refresh access token",
)
class RefreshView(TokenRefreshView):
    """JWT refresh endpoint."""


@extend_schema(
    tags=["Authentication"],
    summary="Get current authenticated user",
    responses=UserSerializer,
)
class CurrentUserView(APIView):
    """Return the current authenticated user's details."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)



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
