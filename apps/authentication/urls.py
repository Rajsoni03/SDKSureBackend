from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewsets import UserViewSet
from .views import CurrentUserView, LoginView, RefreshView

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/login/", LoginView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", RefreshView.as_view(), name="token_refresh"),
    path("auth/me/", CurrentUserView.as_view(), name="auth_me"),
]
