"""PAME recommendation tests for the TechNest demo catalog orders."""

from decimal import Decimal

from django.core.management import call_command
from django.test import TestCase

from orders.models import Order
from recommendations.models import RecommendationStatus
from recommendations.services import RecommendationService


class PAMEDemoOrderTests(TestCase):
    """Verify sample orders match expected boxes under the PAME algorithm."""

    EXPECTED_BOXES = {
        "ORD001": "BX-S01",
        "ORD002": "BX-S01",
        "ORD003": "BX-L01",
        "ORD004": "BX-L01",
        "ORD005": "BX-M01",
        "ORD006": "BX-M01",
        "ORD007": "BX-M01",
        "ORD008": "BX-XL01",
        "ORD009": "BX-XL01",
        "ORD010": "BX-XL01",
    }

    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data")

    def test_demo_orders_recommend_expected_boxes(self):
        for order_number, expected_box_code in self.EXPECTED_BOXES.items():
            with self.subTest(order_number=order_number):
                order = Order.objects.get(order_number=order_number)
                recommendation = RecommendationService.recommend_for_order(order)
                self.assertEqual(recommendation.status, RecommendationStatus.SUCCESS)
                self.assertIsNotNone(recommendation.recommended_box)
                self.assertEqual(
                    recommendation.recommended_box.box_code,
                    expected_box_code,
                )

    def test_ord010_pame_envelope_selects_xl_not_heavy_duty(self):
        order = Order.objects.get(order_number="ORD010")
        recommendation = RecommendationService.recommend_for_order(order)
        self.assertEqual(recommendation.recommended_box.box_code, "BX-XL01")
        self.assertEqual(recommendation.required_length, Decimal("12.00"))
        self.assertEqual(recommendation.required_width, Decimal("38.00"))
        self.assertEqual(recommendation.required_height, Decimal("60.00"))
