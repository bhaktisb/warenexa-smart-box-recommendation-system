"""Django admin registrations for orders."""

from django.contrib import admin

from orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    autocomplete_fields = ("product",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "customer_name", "order_date", "status", "created_at")
    list_filter = ("status", "order_date")
    search_fields = ("order_number", "customer_name")
    ordering = ("-order_date", "-created_at")
    inlines = [OrderItemInline]
    list_per_page = 25


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "created_at")
    list_filter = ("order__status",)
    search_fields = ("order__order_number", "product__sku", "product__name")
    ordering = ("-created_at",)
    autocomplete_fields = ("order", "product")
