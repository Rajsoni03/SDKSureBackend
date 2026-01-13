#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
from pathlib import Path
import sys

from dotenv import load_dotenv

# Load environment variables from local .env if present
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Ensure key environment defaults are set before Django loads settings
os.environ.setdefault("DJANGO_ENV", "development")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


def _debug_env():
    """Print key environment values to help debug startup issues."""
    debug_flag = os.getenv("MANAGE_DEBUG", "true").lower() == "true"
    if not debug_flag:
        return

    print(f"[manage.py] cwd: {Path.cwd()}")
    print(f"[manage.py] BASE_DIR: {BASE_DIR}")
    print(f"[manage.py] DJANGO_ENV: {os.getenv('DJANGO_ENV')}")
    print(f"[manage.py] DEBUG env: {os.getenv('DEBUG')}")
    print(f"[manage.py] ALLOWED_HOSTS env: {os.getenv('ALLOWED_HOSTS')}")
    print(f"[manage.py] DJANGO_SETTINGS_MODULE: {os.getenv('DJANGO_SETTINGS_MODULE')}")


def main():
    """Run administrative tasks."""
    _debug_env()
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
