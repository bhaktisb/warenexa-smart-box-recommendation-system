"""Unit tests for order models."""

from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from orders.models import Order, OrderItem
from products.models import Product


class OrderModelTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            sku="SKU-100",
            name="USB Cable",
            category="Accessories",
            price=Decimal("9.99"),
            length=Decimal("15"),
            width=Decimal("10"),
            height=Decimal("3"),
            weight=Decimal("0.200"),
        )
        self.order = Order.objects.create(
            order_number="ORD-1001",
            customer_name="Jane Doe",
            order_date=date.today(),
        )

    def test_create_order_with_items(self):
        OrderItem.objects.create(order=self.order, product=self.product, quantity=2)
        self.assertEqual(self.order.items.count(), 1)

    def test_reject_invalid_quantity(self):
        item = OrderItem(order=self.order, product=self.product, quantity=0)
        with self.assertRaises(ValidationError):
            item.full_clean()
