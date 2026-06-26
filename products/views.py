"""Presentation layer views for product management."""

from django.views.generic import DetailView, ListView

from core.mixins import StaffRequiredMixin
from products.models import Product


class ProductListView(StaffRequiredMixin, ListView):
    """List active and inactive products for warehouse staff."""

    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 20
    ordering = ["name"]


class ProductDetailView(StaffRequiredMixin, DetailView):
    """Display product details."""

    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"
