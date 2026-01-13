from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewsets import SystemConfigurationViewSet

router = DefaultRouter()
router.register(r"system-configurations", SystemConfigurationViewSet, basename="system-configuration")

urlpatterns = [
    path("", include(router.urls)),
]

