"""Unit tests for OrderService."""

from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from boxes.models import ShippingBox
from orders.models import Order, OrderItem, OrderStatus
from orders.services import OrderService
from products.models import Product
from recommendations.models import BoxRecommendation, RecommendationStatus


class OrderServiceTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            sku="SVC-001",
            name="Service Test Product",
            category="Test",
            price=Decimal("10"),
            length=Decimal("10"),
            width=Decimal("10"),
            height=Decimal("10"),
            weight=Decimal("1"),
        )
        self.order = Order.objects.create(
            order_number="SVC-ORD-1",
            customer_name="Test Customer",
            order_date=date.today(),
        )
        OrderItem.objects.create(order=self.order, product=self.product, quantity=1)
        self.box = ShippingBox.objects.create(
            box_code="SVC-BOX",
            name="Service Test Box",
            length=Decimal("20"),
            width=Decimal("20"),
            height=Decimal("20"),
            max_weight_capacity=Decimal("5"),
            cost=Decimal("10"),
        )

    def test_validate_rejects_empty_order(self):
        empty_order = Order.objects.create(
            order_number="SVC-EMPTY",
            customer_name="Empty",
            order_date=date.today(),
        )
        with self.assertRaises(ValidationError):
            OrderService.validate_order_for_recommendation(empty_order)

    def test_validate_rejects_packed_order(self):
        self.order.status = OrderStatus.PACKED
        self.order.save()
        with self.assertRaises(ValidationError):
            OrderService.validate_order_for_recommendation(self.order)

    def test_validate_rejects_inactive_product(self):
        self.product.is_active = False
        self.product.save()
        with self.assertRaises(ValidationError):
            OrderService.validate_order_for_recommendation(self.order)

    def test_confirm_packing_requires_successful_recommendation(self):
        with self.assertRaises(ValidationError):
            OrderService.confirm_packing(self.order)

    def test_confirm_packing_marks_order_packed(self):
        BoxRecommendation.objects.create(
            order=self.order,
            recommended_box=self.box,
            total_weight=Decimal("1"),
            required_length=Decimal("10"),
            required_width=Decimal("10"),
            required_height=Decimal("10"),
            status=RecommendationStatus.SUCCESS,
            message="ok",
        )
        OrderService.confirm_packing(self.order)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, OrderStatus.PACKED)

    def test_confirm_packing_rejects_already_packed_order(self):
        BoxRecommendation.objects.create(
            order=self.order,
            recommended_box=self.box,
            total_weight=Decimal("1"),
            required_length=Decimal("10"),
            required_width=Decimal("10"),
            required_height=Decimal("10"),
            status=RecommendationStatus.SUCCESS,
            message="ok",
        )
        OrderService.confirm_packing(self.order)
        with self.assertRaises(ValidationError):
            OrderService.confirm_packing(self.order)
