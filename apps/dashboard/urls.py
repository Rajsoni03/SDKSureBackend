from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewsets import DashboardMetricViewSet

router = DefaultRouter()
router.register(r"dashboard-metrics", DashboardMetricViewSet, basename="dashboard-metric")

urlpatterns = [
    path("", include(router.urls)),
]

