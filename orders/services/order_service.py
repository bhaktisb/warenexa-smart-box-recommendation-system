"""Business service layer for warehouse orders."""

from __future__ import annotations

import logging

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from orders.models import Order, OrderStatus

logger = logging.getLogger(__name__)


class OrderService:
    """Encapsulates order validation and packing workflow operations."""

    @staticmethod
    def validate_order_for_recommendation(order: Order) -> None:
        """
        Validate that an order can be processed by the recommendation engine.

        Raises:
            ValidationError: When the order is not eligible for recommendation.
        """
        if not order.items.exists():
            raise ValidationError("Order must contain at least one item.")

        inactive_products = [
            item.product.sku
            for item in order.items.select_related("product")
            if not item.product.is_active
        ]
        if inactive_products:
            raise ValidationError(
                "Order contains inactive products: "
                + ", ".join(sorted(inactive_products))
            )

        if order.status == OrderStatus.PACKED:
            raise ValidationError("Packed orders cannot be re-recommended.")

    @staticmethod
    @transaction.atomic
    def confirm_packing(order: Order) -> Order:
        """
        Confirm warehouse packing for an order with a successful recommendation.

        Raises:
            ValidationError: When packing cannot be confirmed.
        """
        if order.status == OrderStatus.PACKED:
            raise ValidationError("This order has already been packed.")

        latest = (
            order.recommendations.filter(is_confirmed=False)
            .select_related("recommended_box")
            .order_by("-created_at")
            .first()
        )
        if latest is None or latest.recommended_box is None:
            raise ValidationError(
                "A successful box recommendation is required before packing."
            )

        latest.is_confirmed = True
        latest.confirmed_at = timezone.now()
        latest.save(update_fields=["is_confirmed", "confirmed_at"])

        order.status = OrderStatus.PACKED
        order.save(update_fields=["status", "updated_at"])
        logger.info("Packing confirmed for order %s", order.order_number)
        return order
