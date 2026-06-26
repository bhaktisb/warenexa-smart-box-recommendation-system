"""Unit tests for product models."""

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from products.models import Product


class ProductModelTests(TestCase):
    def setUp(self):
        self.product = Product(
            sku="SKU-001",
            name="Wireless Mouse",
            category="Accessories",
            price=Decimal("19.99"),
            length=Decimal("10"),
            width=Decimal("6"),
            height=Decimal("4"),
            weight=Decimal("0.150"),
        )

    def test_create_valid_product(self):
        self.product.full_clean()
        self.product.save()
        self.assertEqual(Product.objects.count(), 1)

    def test_reject_negative_dimensions(self):
        self.product.length = Decimal("-1")
        with self.assertRaises(ValidationError):
            self.product.full_clean()

    def test_reject_duplicate_sku(self):
        self.product.save()
        duplicate = Product(
            sku="SKU-001",
            name="Duplicate",
            category="Accessories",
            price=Decimal("10"),
            length=Decimal("1"),
            width=Decimal("1"),
            height=Decimal("1"),
            weight=Decimal("1"),
        )
        with self.assertRaises(Exception):
            duplicate.save()
