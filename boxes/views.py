"""Presentation layer views for shipping box management."""

from django.views.generic import DetailView, ListView

from boxes.models import ShippingBox
from core.mixins import StaffRequiredMixin


class ShippingBoxListView(StaffRequiredMixin, ListView):
    """List available shipping boxes."""

    model = ShippingBox
    template_name = "boxes/box_list.html"
    context_object_name = "boxes"
    paginate_by = 20
    ordering = ["cost", "box_code"]


class ShippingBoxDetailView(StaffRequiredMixin, DetailView):
    """Display shipping box details."""

    model = ShippingBox
    template_name = "boxes/box_detail.html"
    context_object_name = "box"
