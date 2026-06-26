"""View tests for warehouse order workflow."""

from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from boxes.models import ShippingBox
from orders.models import Order, OrderItem, OrderStatus
from products.models import Product
from recommendations.models import BoxRecommendation, RecommendationStatus


class OrderViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff = User.objects.create_user(
            username="warehouse",
            password="secure-pass-123",
            is_staff=True,
        )
        self.product = Product.objects.create(
            sku="VIEW-001",
            name="View Test Mouse",
            category="Test",
            price=Decimal("100"),
            length=Decimal("11"),
            width=Decimal("6"),
            height=Decimal("4"),
            weight=Decimal("0.12"),
        )
        self.box = ShippingBox.objects.create(
            box_code="VIEW-BOX",
            name="View Test Box",
            length=Decimal("20"),
            width=Decimal("15"),
            height=Decimal("10"),
            max_weight_capacity=Decimal("1"),
            cost=Decimal("30"),
        )
        self.order = Order.objects.create(
            order_number="VIEW-ORD-1",
            customer_name="View Customer",
            order_date=date.today(),
        )
        OrderItem.objects.create(order=self.order, product=self.product, quantity=1)

    def test_order_list_requires_staff_login(self):
        response = self.client.get(reverse("orders:list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_recommend_box_requires_staff_login(self):
        response = self.client.post(reverse("orders:recommend", kwargs={"pk": self.order.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_recommend_box_success(self):
        self.client.login(username="warehouse", password="secure-pass-123")
        response = self.client.post(reverse("orders:recommend", kwargs={"pk": self.order.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            BoxRecommendation.objects.filter(
                order=self.order,
                status=RecommendationStatus.SUCCESS,
            ).exists()
        )

    def test_confirm_packing_success(self):
        self.client.login(username="warehouse", password="secure-pass-123")
        BoxRecommendation.objects.create(
            order=self.order,
            recommended_box=self.box,
            total_weight=Decimal("0.12"),
            required_length=Decimal("4"),
            required_width=Decimal("6"),
            required_height=Decimal("11"),
            status=RecommendationStatus.SUCCESS,
            message="ok",
        )
        response = self.client.post(
            reverse("orders:confirm_packing", kwargs={"pk": self.order.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, OrderStatus.PACKED)
