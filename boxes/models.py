"""Shipping box models for warehouse packing."""

from django.core.exceptions import ValidationError
from django.db import models

from core.models import ValidatedModel
from core.validators import validate_positive_decimal


class ShippingBox(ValidatedModel):
    """An available shipping box with internal dimensions and cost."""

    box_code = models.CharField(max_length=50, unique=True, db_index=True)
    name = models.CharField(max_length=100, default="")
    length = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[validate_positive_decimal],
        help_text="Internal length in centimeters.",
    )
    width = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[validate_positive_decimal],
        help_text="Internal width in centimeters.",
    )
    height = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[validate_positive_decimal],
        help_text="Internal height in centimeters.",
    )
    max_weight_capacity = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        validators=[validate_positive_decimal],
        help_text="Maximum weight capacity in kilograms.",
    )
    cost = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[validate_positive_decimal],
        help_text="Shipping box cost.",
    )
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["cost", "box_code"]
        verbose_name = "shipping box"
        verbose_name_plural = "shipping boxes"

    def __str__(self) -> str:
        return f"{self.box_code} - {self.name}"

    def clean(self) -> None:
        super().clean()
        if not self.name.strip():
            raise ValidationError({"name": "Box name is required."})
