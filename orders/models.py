"""Warehouse order models."""

from django.core.validators import MinValueValidator
from django.db import models

from core.models import ValidatedModel


class OrderStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    RECOMMENDED = "recommended", "Recommended"
    PACKED = "packed", "Packed"
    DISPATCHED = "dispatched", "Dispatched"


class Order(models.Model):
    """A warehouse order awaiting packing."""

    order_number = models.CharField(max_length=50, unique=True, db_index=True)
    customer_name = models.CharField(max_length=200)
    order_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-order_date", "-created_at"]

    def __str__(self) -> str:
        return self.order_number


class OrderItem(ValidatedModel):
    """A line item linking a product to an order."""

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.PROTECT,
        related_name="order_items",
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        default=1,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(
                fields=["order", "product"],
                name="unique_order_product",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.order.order_number} - {self.product.sku} x {self.quantity}"
