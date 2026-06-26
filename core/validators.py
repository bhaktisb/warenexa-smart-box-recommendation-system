"""Shared field validators for warehouse domain models."""

from decimal import Decimal

from django.core.exceptions import ValidationError


def validate_positive_decimal(value: Decimal) -> None:
    """Ensure a decimal value is strictly greater than zero."""
    if value is None or value <= 0:
        raise ValidationError("Value must be greater than zero.")


def validate_non_negative_decimal(value: Decimal) -> None:
    """Ensure a decimal value is zero or greater."""
    if value is None or value < 0:
        raise ValidationError("Value cannot be negative.")
