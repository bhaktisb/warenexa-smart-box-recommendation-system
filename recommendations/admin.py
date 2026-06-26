"""Django admin registrations for box recommendations."""

from django.contrib import admin

from recommendations.models import BoxRecommendation


@admin.register(BoxRecommendation)
class BoxRecommendationAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "recommended_box",
        "status",
        "total_weight",
        "is_confirmed",
        "created_at",
    )
    list_filter = ("status", "is_confirmed", "created_at")
    search_fields = ("order__order_number", "recommended_box__box_code", "message")
    ordering = ("-created_at",)
    readonly_fields = (
        "order",
        "recommended_box",
        "total_weight",
        "required_length",
        "required_width",
        "required_height",
        "status",
        "message",
        "created_at",
        "confirmed_at",
    )
    list_per_page = 25
