"""Unit tests for shipping box models."""

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from boxes.models import ShippingBox


class ShippingBoxModelTests(TestCase):
    def setUp(self):
        self.box = ShippingBox(
            box_code="BOX-S",
            name="Small Box",
            length=Decimal("30"),
            width=Decimal("20"),
            height=Decimal("15"),
            max_weight_capacity=Decimal("5"),
            cost=Decimal("2.50"),
        )

    def test_create_valid_box(self):
        self.box.full_clean()
        self.box.save()
        self.assertEqual(ShippingBox.objects.count(), 1)

    def test_reject_negative_cost(self):
        self.box.cost = Decimal("-1")
        with self.assertRaises(ValidationError):
            self.box.full_clean()

    def test_reject_empty_box_name(self):
        self.box.name = "   "
        with self.assertRaises(ValidationError):
            self.box.full_clean()

    def test_reject_duplicate_box_code(self):
        self.box.save()
        duplicate = ShippingBox(
            box_code="BOX-S",
            name="Duplicate Box",
            length=Decimal("10"),
            width=Decimal("10"),
            height=Decimal("10"),
            max_weight_capacity=Decimal("1"),
            cost=Decimal("1"),
        )
        with self.assertRaises(Exception):
            duplicate.save()
