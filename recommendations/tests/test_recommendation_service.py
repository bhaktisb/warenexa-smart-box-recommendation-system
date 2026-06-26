"""Unit tests for the recommendation engine."""

from datetime import date
from decimal import Decimal

from django.test import TestCase

from boxes.models import ShippingBox
from orders.models import Order, OrderItem, OrderStatus
from products.models import Product
from recommendations.models import RecommendationStatus
from recommendations.services import RecommendationService


class RecommendationServiceTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            sku="SKU-200",
            name="Bluetooth Speaker",
            category="Audio",
            price=Decimal("49.99"),
            length=Decimal("18"),
            width=Decimal("8"),
            height=Decimal("8"),
            weight=Decimal("0.600"),
        )
        self.small_box = ShippingBox.objects.create(
            box_code="BOX-SM",
            name="Small Test Box",
            length=Decimal("20"),
            width=Decimal("15"),
            height=Decimal("10"),
            max_weight_capacity=Decimal("2"),
            cost=Decimal("3.00"),
        )
        self.large_box = ShippingBox.objects.create(
            box_code="BOX-LG",
            name="Large Test Box",
            length=Decimal("30"),
            width=Decimal("25"),
            height=Decimal("40"),
            max_weight_capacity=Decimal("10"),
            cost=Decimal("5.00"),
        )
        self.cheap_large_box = ShippingBox.objects.create(
            box_code="BOX-MD",
            name="Medium Test Box",
            length=Decimal("30"),
            width=Decimal("25"),
            height=Decimal("40"),
            max_weight_capacity=Decimal("10"),
            cost=Decimal("4.00"),
        )
        self.order = Order.objects.create(
            order_number="ORD-2001",
            customer_name="John Smith",
            order_date=date.today(),
        )
        OrderItem.objects.create(order=self.order, product=self.product, quantity=2)

    def test_calculate_total_weight(self):
        items = list(self.order.items.select_related("product"))
        total = RecommendationService.calculate_total_weight(items)
        self.assertEqual(total, Decimal("1.200"))

    def test_selects_lowest_cost_qualifying_box(self):
        recommendation = RecommendationService.recommend_for_order(self.order)
        self.assertEqual(recommendation.status, RecommendationStatus.SUCCESS)
        self.assertEqual(recommendation.recommended_box, self.small_box)
        self.assertEqual(
            (recommendation.required_length, recommendation.required_width, recommendation.required_height),
            (Decimal("8"), Decimal("8"), Decimal("18")),
        )
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, OrderStatus.RECOMMENDED)

    def test_returns_no_suitable_box_when_weight_exceeds_capacity(self):
        heavy_product = Product.objects.create(
            sku="SKU-HEAVY",
            name="Heavy Item",
            category="Equipment",
            price=Decimal("199.99"),
            length=Decimal("10"),
            width=Decimal("10"),
            height=Decimal("10"),
            weight=Decimal("15.000"),
        )
        order = Order.objects.create(
            order_number="ORD-HEAVY",
            customer_name="Warehouse",
            order_date=date.today(),
        )
        OrderItem.objects.create(order=order, product=heavy_product, quantity=1)

        recommendation = RecommendationService.recommend_for_order(order)
        self.assertEqual(recommendation.status, RecommendationStatus.NO_SUITABLE_BOX)
        self.assertIsNone(recommendation.recommended_box)
        self.assertEqual(
            recommendation.message,
            RecommendationService.NO_SUITABLE_BOX_MESSAGE,
        )

    def test_box_passes_weight_validation(self):
        self.assertTrue(
            RecommendationService.box_passes_weight_validation(
                self.large_box,
                Decimal("5"),
            )
        )
        self.assertFalse(
            RecommendationService.box_passes_weight_validation(
                self.small_box,
                Decimal("5"),
            )
        )

    def test_box_passes_dimension_validation(self):
        required = (Decimal("8"), Decimal("8"), Decimal("18"))
        units = [(Decimal("18"), Decimal("8"), Decimal("8"))] * 2
        self.assertTrue(
            RecommendationService.box_passes_dimension_validation(
                self.small_box,
                required,
                units,
            )
        )
        narrow_box = ShippingBox.objects.create(
            box_code="BOX-NARROW",
            name="Narrow Test Box",
            length=Decimal("15"),
            width=Decimal("10"),
            height=Decimal("8"),
            max_weight_capacity=Decimal("5"),
            cost=Decimal("2.00"),
        )
        self.assertFalse(
            RecommendationService.box_passes_dimension_validation(
                narrow_box,
                required,
                units,
            )
        )
