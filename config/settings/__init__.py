"""Environment-aware settings loader."""
import os

ENVIRONMENT = os.getenv("DJANGO_ENV", "development").lower()

if ENVIRONMENT == "production":
    from .production import *  # noqa: F401,F403
elif ENVIRONMENT in ("test", "testing"):
    from .testing import *  # noqa: F401,F403
else:
    from .development import *  # noqa: F401,F403

