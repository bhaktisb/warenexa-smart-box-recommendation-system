"""
Box recommendation engine service.

Orchestrates validation, weight and dimension calculations, box filtering,
and lowest-cost selection while keeping business logic out of views and models.
"""

from __future__ import annotations

import logging
from decimal import Decimal

from django.db import transaction

from boxes.models import ShippingBox
from core.utils.dimensions import (
    calculate_required_dimensions,
    expand_order_units,
)
from orders.models import Order, OrderStatus
from orders.services.order_service import OrderService
from recommendations.models import BoxRecommendation, RecommendationStatus

logger = logging.getLogger(__name__)


class RecommendationService:
    """Service responsible for generating shipping box recommendations."""

    NO_SUITABLE_BOX_MESSAGE = "No Suitable Box Available"

    @classmethod
    @transaction.atomic
    def recommend_for_order(cls, order: Order) -> BoxRecommendation:
        """
        Execute the recommendation workflow for a warehouse order.

        Steps:
            1. Validate order eligibility.
            2. Calculate total order weight.
            3. Calculate required dimensions (PAME envelope).
            4. Retrieve active shipping boxes.
            5. Remove boxes failing dimension validation.
            6. Remove boxes exceeding maximum weight capacity.
            7. Select the lowest-cost qualifying box.
            8. Persist and return the recommendation outcome.
        """
        OrderService.validate_order_for_recommendation(order)

        order_items = list(order.items.select_related("product"))
        total_weight = cls.calculate_total_weight(order_items)
        units = expand_order_units(order_items)
        required_dims = calculate_required_dimensions(units)

        selected_box = cls.select_best_box(
            total_weight=total_weight,
            required_dims=required_dims,
            units=units,
        )

        if selected_box is None:
            logger.warning(
                "No suitable box for order %s (weight=%s, envelope=%s)",
                order.order_number,
                total_weight,
                required_dims,
            )
            recommendation = BoxRecommendation.objects.create(
                order=order,
                total_weight=total_weight,
                required_length=required_dims[0],
                required_width=required_dims[1],
                required_height=required_dims[2],
                status=RecommendationStatus.NO_SUITABLE_BOX,
                message=cls.NO_SUITABLE_BOX_MESSAGE,
            )
        else:
            logger.info(
                "Recommended box %s for order %s",
                selected_box.box_code,
                order.order_number,
            )
            recommendation = BoxRecommendation.objects.create(
                order=order,
                recommended_box=selected_box,
                total_weight=total_weight,
                required_length=required_dims[0],
                required_width=required_dims[1],
                required_height=required_dims[2],
                status=RecommendationStatus.SUCCESS,
                message=(
                    f"Recommended box {selected_box.box_code} "
                    f"at cost {selected_box.cost}."
                ),
            )
            order.status = OrderStatus.RECOMMENDED
            order.save(update_fields=["status", "updated_at"])

        return recommendation

    @staticmethod
    def calculate_total_weight(order_items) -> Decimal:
        """Calculate aggregate order weight from line items."""
        total = Decimal("0")
        for item in order_items:
            total += item.product.weight * item.quantity
        return total

    @staticmethod
    def select_best_box(
        total_weight: Decimal,
        required_dims: tuple[Decimal, Decimal, Decimal],
        units: list[tuple[Decimal, Decimal, Decimal]],
    ) -> ShippingBox | None:
        """Return the lowest-cost active box that passes all validation rules."""
        for box in ShippingBox.objects.filter(is_active=True).order_by("cost", "box_code"):
            if not RecommendationService.box_passes_weight_validation(box, total_weight):
                continue
            if not RecommendationService.box_passes_dimension_validation(
                box, required_dims, units
            ):
                continue
            return box
        return None

    @staticmethod
    def box_passes_dimension_validation(
        box: ShippingBox,
        required_dims: tuple[Decimal, Decimal, Decimal],
        units: list[tuple[Decimal, Decimal, Decimal]],
    ) -> bool:
        """Expose dimension validation for unit testing and diagnostics."""
        from core.utils.dimensions import dimensions_fit, item_fits_in_box, sort_dimensions

        box_dims = sort_dimensions(box.length, box.width, box.height)
        if not dimensions_fit(required_dims, box_dims):
            return False

        return all(
            item_fits_in_box(
                unit[0],
                unit[1],
                unit[2],
                box.length,
                box.width,
                box.height,
            )
            for unit in units
        )

    @staticmethod
    def box_passes_weight_validation(box: ShippingBox, total_weight: Decimal) -> bool:
        """Expose weight validation for unit testing and diagnostics."""
        return total_weight <= box.max_weight_capacity
