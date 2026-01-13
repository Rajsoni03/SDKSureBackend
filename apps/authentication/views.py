from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import UserSerializer


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
