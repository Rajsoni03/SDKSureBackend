"""Custom exception handling."""
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """Delegate to DRF with room for customization."""
    response = exception_handler(exc, context)
    return response

