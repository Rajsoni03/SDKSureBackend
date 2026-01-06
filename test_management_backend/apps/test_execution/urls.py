from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewsets import TestRunViewSet, TestScenarioViewSet

router = DefaultRouter()
router.register(r"test-runs", TestRunViewSet, basename="test-run")
router.register(r"test-scenarios", TestScenarioViewSet, basename="test-scenario")

urlpatterns = [
    path("", include(router.urls)),
]
