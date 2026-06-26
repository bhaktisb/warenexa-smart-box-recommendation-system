"""Presentation layer views for warehouse order management."""

import logging

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView, View

from core.mixins import StaffRequiredMixin
from orders.models import Order, OrderStatus
from orders.services import OrderService
from recommendations.services import RecommendationService

logger = logging.getLogger(__name__)


class OrderListView(StaffRequiredMixin, ListView):
    """List warehouse orders."""

    model = Order
    template_name = "orders/order_list.html"
    context_object_name = "orders"
    paginate_by = 20
    ordering = ["-order_date", "-created_at"]


class OrderDetailView(StaffRequiredMixin, DetailView):
    """Display order details and recommendation actions."""

    model = Order
    template_name = "orders/order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        return Order.objects.prefetch_related("items__product")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_recommendation"] = (
            self.object.recommendations.select_related("recommended_box")
            .order_by("-created_at")
            .first()
        )
        context["order_status_packed"] = OrderStatus.PACKED
        return context


class RecommendBoxView(StaffRequiredMixin, View):
    """Trigger the recommendation engine for an order."""

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        try:
            recommendation = RecommendationService.recommend_for_order(order)
            if recommendation.recommended_box:
                messages.success(
                    request,
                    f"Recommended box: {recommendation.recommended_box.box_code}",
                )
            else:
                messages.warning(request, recommendation.message)
        except ValidationError as exc:
            messages.error(request, "; ".join(getattr(exc, "messages", [str(exc)])))
        except Exception:
            logger.exception("Recommendation failed for order pk=%s", pk)
            messages.error(
                request,
                "An unexpected error occurred while generating the recommendation.",
            )
        return redirect(reverse("orders:detail", kwargs={"pk": pk}))


class ConfirmPackingView(StaffRequiredMixin, View):
    """Confirm warehouse packing after a successful recommendation."""

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        try:
            OrderService.confirm_packing(order)
            messages.success(request, "Packing confirmed successfully.")
        except ValidationError as exc:
            messages.error(request, "; ".join(getattr(exc, "messages", [str(exc)])))
        except Exception:
            logger.exception("Confirm packing failed for order pk=%s", pk)
            messages.error(
                request,
                "An unexpected error occurred while confirming packing.",
            )
        return redirect(reverse("orders:detail", kwargs={"pk": pk}))
