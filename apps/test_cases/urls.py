from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewsets import LabelViewSet, TestCaseViewSet, TestTypeViewSet

router = DefaultRouter()
router.register(r"test-cases", TestCaseViewSet, basename="test-case")
router.register(r"test-types", TestTypeViewSet, basename="test-type")
router.register(r"labels", LabelViewSet, basename="label")

urlpatterns = [
    path("", include(router.urls)),
]
