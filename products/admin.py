"""Django admin registrations for products."""

from django.contrib import admin

from products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "sku",
        "name",
        "category",
        "price",
        "length",
        "width",
        "height",
        "weight",
        "is_active",
    )
    list_filter = ("is_active", "category")
    search_fields = ("sku", "name", "category")
    ordering = ("name",)
    list_per_page = 25
