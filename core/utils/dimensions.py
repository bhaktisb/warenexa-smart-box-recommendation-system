"""
Dimension utilities for the box recommendation engine.

PAME — Per-Axis Maximum Envelope
--------------------------------
Warehouse packing is a complex 3D bin-packing problem. This module uses PAME, a
documented simplification suitable for academic warehouse management systems:

1. Each product unit may be rotated freely inside the box.
2. For every unit, dimensions are sorted ascending: d1 <= d2 <= d3.
3. Combined order envelope (PAME):
   - required_d1 = max(d1) across all units
   - required_d2 = max(d2) across all units
   - required_d3 = max(d3) across all units
4. A box satisfies the envelope when its sorted internal dimensions are greater
   than or equal to the required sorted dimensions.
5. Additionally, every individual unit must fit inside the box (rotation-aware).

Assumption: smaller items are packed into void space within the largest item's
bounding prism (typical consumer-electronics fulfillment). This model does not
handle two equally large items that each require separate floor space.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Iterable, Sequence

Dimensions = tuple[Decimal, Decimal, Decimal]


def sort_dimensions(length: Decimal, width: Decimal, height: Decimal) -> Dimensions:
    """Return length, width, and height sorted from smallest to largest."""
    return tuple(sorted((length, width, height), key=lambda value: value))


def dimensions_fit(required: Dimensions, container: Dimensions) -> bool:
    """Return True when required sorted dimensions fit inside container sorted dimensions."""
    return all(req <= cap for req, cap in zip(required, container))


def item_fits_in_box(
    item_length: Decimal,
    item_width: Decimal,
    item_height: Decimal,
    box_length: Decimal,
    box_width: Decimal,
    box_height: Decimal,
) -> bool:
    """Check whether a single item fits in a box with arbitrary rotation."""
    return dimensions_fit(
        sort_dimensions(item_length, item_width, item_height),
        sort_dimensions(box_length, box_width, box_height),
    )


def calculate_required_dimensions(
    units: Iterable[Sequence[Decimal]],
) -> Dimensions:
    """
    Calculate the PAME required envelope for a collection of product units.

    Each unit is a sequence of (length, width, height). Returns the per-axis
    maximum of sorted unit dimensions: (max d1, max d2, max d3).
    """
    max_d1 = Decimal("0")
    max_d2 = Decimal("0")
    max_d3 = Decimal("0")

    for length, width, height in units:
        d1, d2, d3 = sort_dimensions(length, width, height)
        max_d1 = max(max_d1, d1)
        max_d2 = max(max_d2, d2)
        max_d3 = max(max_d3, d3)

    return max_d1, max_d2, max_d3


def expand_order_units(order_items: Iterable) -> list[Dimensions]:
    """
    Expand order line items into individual units for dimension calculations.

    Each order item must expose ``product`` with length/width/height and a
    positive ``quantity``.
    """
    units: list[Dimensions] = []
    for item in order_items:
        product = item.product
        unit = (product.length, product.width, product.height)
        units.extend([unit] * item.quantity)
    return units
