"""Product catalog models for warehouse packing."""

from django.db import models

from core.models import ValidatedModel
from core.validators import validate_non_negative_decimal, validate_positive_decimal


class Product(ValidatedModel):
    """A sellable product with physical dimensions and weight."""

    sku = models.CharField(max_length=50, unique=True, db_index=True)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, db_index=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[validate_non_negative_decimal],
    )
    length = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[validate_positive_decimal],
        help_text="Length in centimeters.",
    )
    width = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[validate_positive_decimal],
        help_text="Width in centimeters.",
    )
    height = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[validate_positive_decimal],
        help_text="Height in centimeters.",
    )
    weight = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        validators=[validate_positive_decimal],
        help_text="Weight in kilograms.",
    )
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["category", "is_active"]),
        ]

    def __str__(self) -> str:
        return f"{self.sku} - {self.name}"
