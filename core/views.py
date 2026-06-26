"""Presentation layer views for the warehouse dashboard."""

from django.views.generic import TemplateView

from boxes.models import ShippingBox
from core.mixins import StaffRequiredMixin
from orders.models import Order, OrderStatus
from products.models import Product
from recommendations.models import BoxRecommendation, RecommendationStatus


class DashboardView(StaffRequiredMixin, TemplateView):
    """Warehouse landing page with operational summary metrics."""

    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "product_count": Product.objects.filter(is_active=True).count(),
                "box_count": ShippingBox.objects.filter(is_active=True).count(),
                "order_count": Order.objects.count(),
                "pending_order_count": Order.objects.filter(
                    status=OrderStatus.PENDING
                ).count(),
                "recommendation_count": BoxRecommendation.objects.count(),
                "successful_recommendation_count": BoxRecommendation.objects.filter(
                    status=RecommendationStatus.SUCCESS
                ).count(),
                "recent_orders": Order.objects.order_by("-order_date", "-created_at")[:5],
                "recent_recommendations": BoxRecommendation.objects.select_related(
                    "order", "recommended_box"
                ).order_by("-created_at")[:5],
            }
        )
        return context
