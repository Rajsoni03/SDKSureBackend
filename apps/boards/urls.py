from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewsets import (
    BoardViewSet,
    CapabilityViewSet,
    PCStatsViewSet,
    RelayViewSet,
    TestPCViewSet,
)

router = DefaultRouter()
router.register(r"boards", BoardViewSet, basename="board")
router.register(r"capabilities", CapabilityViewSet, basename="capability")
router.register(r"relays", RelayViewSet, basename="relay")
router.register(r"test-pcs", TestPCViewSet, basename="test-pc")
router.register(r"pc-stats", PCStatsViewSet, basename="pc-stats")

urlpatterns = [
    path("", include(router.urls)),
]
