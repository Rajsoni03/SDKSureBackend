"""ASGI config for test_management_backend project with Channels support."""
import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django_asgi_app = get_asgi_application()


# Lazy import to avoid settings issues during startup
def websocket_urlpatterns():
    try:
        from apps.realtime.routing import websocket_urlpatterns as realtime_patterns
    except Exception:
        realtime_patterns = []
    return [*realtime_patterns]


application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": URLRouter(websocket_urlpatterns()),
    }
)
