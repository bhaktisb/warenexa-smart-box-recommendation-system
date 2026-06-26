"""Django admin registrations for shipping boxes."""

from django.contrib import admin

from boxes.models import ShippingBox


@admin.register(ShippingBox)
class ShippingBoxAdmin(admin.ModelAdmin):
    list_display = (
        "box_code",
        "name",
        "length",
        "width",
        "height",
        "max_weight_capacity",
        "cost",
        "is_active",
    )
    list_filter = ("is_active",)
    search_fields = ("box_code", "name")
    ordering = ("cost", "box_code")
    list_per_page = 25
