"""Production settings."""
from .base import *  # noqa: F401,F403

DEBUG = False
ALLOWED_HOSTS = (
    [host for host in os.getenv("ALLOWED_HOSTS", "").split(",") if host]  # type: ignore[name-defined]
    or ["localhost", "127.0.0.1"]
)

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "0"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "True") == "True"

LOGGING["handlers"]["file"] = {  # type: ignore[name-defined]
    "class": "logging.handlers.RotatingFileHandler",
    "filename": BASE_DIR / "logs" / "django.log",  # type: ignore[name-defined]
    "maxBytes": 10 * 1024 * 1024,
    "backupCount": 5,
    "formatter": "verbose",
}
LOGGING["formatters"] = {  # type: ignore[name-defined]
    "verbose": {
        "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
        "style": "{",
    }
}
LOGGING["root"]["handlers"] = ["console", "file"]  # type: ignore[name-defined]
