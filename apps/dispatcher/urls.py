from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewsets import DispatcherViewSet

router = DefaultRouter()
router.register(r"dispatcher", DispatcherViewSet, basename="dispatcher")

urlpatterns = [
    path("", include(router.urls)),
]
