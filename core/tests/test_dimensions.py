"""Unit tests for dimension utilities."""

from decimal import Decimal

from django.test import SimpleTestCase

from core.utils.dimensions import (
    calculate_required_dimensions,
    dimensions_fit,
    item_fits_in_box,
    sort_dimensions,
)


class DimensionUtilityTests(SimpleTestCase):
    def test_sort_dimensions_orders_values(self):
        self.assertEqual(
            sort_dimensions(Decimal("30"), Decimal("10"), Decimal("20")),
            (Decimal("10"), Decimal("20"), Decimal("30")),
        )

    def test_item_fits_in_box_with_rotation(self):
        self.assertTrue(
            item_fits_in_box(
                Decimal("30"),
                Decimal("10"),
                Decimal("20"),
                Decimal("20"),
                Decimal("30"),
                Decimal("10"),
            )
        )

    def test_item_does_not_fit_in_box(self):
        self.assertFalse(
            item_fits_in_box(
                Decimal("40"),
                Decimal("20"),
                Decimal("10"),
                Decimal("30"),
                Decimal("20"),
                Decimal("10"),
            )
        )

    def test_calculate_required_dimensions_uses_per_axis_maximum_envelope(self):
        units = [
            (Decimal("10"), Decimal("20"), Decimal("30")),
            (Decimal("10"), Decimal("20"), Decimal("30")),
        ]
        self.assertEqual(
            calculate_required_dimensions(units),
            (Decimal("10"), Decimal("20"), Decimal("30")),
        )

    def test_pame_envelope_for_monitor_and_keyboard(self):
        """ORD010 envelope: max per axis, not stacked sum of longest edges."""
        units = [
            (Decimal("60"), Decimal("38"), Decimal("12")),
            (Decimal("45"), Decimal("16"), Decimal("4")),
        ]
        self.assertEqual(
            calculate_required_dimensions(units),
            (Decimal("12"), Decimal("38"), Decimal("60")),
        )

    def test_dimensions_fit_compares_sorted_values(self):
        required = (Decimal("10"), Decimal("20"), Decimal("30"))
        container = (Decimal("15"), Decimal("25"), Decimal("35"))
        self.assertTrue(dimensions_fit(required, container))

        tight_container = (Decimal("10"), Decimal("20"), Decimal("29"))
        self.assertFalse(dimensions_fit(required, tight_container))
