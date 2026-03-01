from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r"users", views.UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
    path("login/", views.LoginView.as_view(), name="token_obtain_pair"),
    path("refresh/", views.RefreshView.as_view(), name="token_refresh"),
    path("me/", views.CurrentUserView.as_view(), name="auth_me"),
]
