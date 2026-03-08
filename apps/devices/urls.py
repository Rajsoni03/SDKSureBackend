from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CapabilityViewSet, RelayViewSet, BoardViewSet, WorkstationViewSet

router = DefaultRouter()
router.register(r"capabilities", CapabilityViewSet, basename="capability")
router.register(r"relays", RelayViewSet, basename="relay")
router.register(r"boards", BoardViewSet, basename="board")
router.register(r"workstations", WorkstationViewSet, basename="workstation")

urlpatterns = [
    path("", include(router.urls)),
]