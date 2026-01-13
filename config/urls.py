"""Root URL configuration."""
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from django.conf import settings

from apps.authentication.urls import router as auth_router
from apps.boards.urls import router as boards_router
from apps.test_cases.urls import router as test_cases_router
from apps.test_execution.urls import router as test_execution_router
from apps.dashboard.urls import router as dashboard_router
from apps.configuration.urls import router as configuration_router
from apps.dispatcher.urls import router as dispatcher_router
from rest_framework.permissions import AllowAny
from apps.authentication.views import CurrentUserView, LoginView, RefreshView

router = DefaultRouter()
for r in [
    auth_router,
    boards_router,
    test_cases_router,
    test_execution_router,
    dashboard_router,
    configuration_router,
    dispatcher_router,
]:
    for prefix, viewset, basename in r.registry:
        router.register(prefix, viewset, basename=basename)


def healthcheck(_request):
    """Simple healthcheck endpoint."""
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
    path("api/v1/auth/login/", LoginView.as_view(), name="api_token_obtain_pair"),
    path("api/v1/auth/refresh/", RefreshView.as_view(), name="api_token_refresh"),
    path("api/v1/auth/me/", CurrentUserView.as_view(), name="api_auth_me"),
    path("health/", healthcheck, name="healthcheck"),
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/v1/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/v1/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

# if settings.DEBUG:
    # try:
        # import debug_toolbar
        # urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
    # except Exception:
    #     pass
