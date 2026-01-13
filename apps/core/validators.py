"""Reusable validators."""
from django.core.exceptions import ValidationError


def validate_uart_port(value: str):
    if not value:
        raise ValidationError("UART port cannot be empty.")
    return value

