"""Box recommendation persistence models."""

from django.db import models


class RecommendationStatus(models.TextChoices):
    SUCCESS = "success", "Success"
    NO_SUITABLE_BOX = "no_suitable_box", "No Suitable Box Available"


class BoxRecommendation(models.Model):
    """Stores the outcome of a recommendation run for an order."""

    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="recommendations",
    )
    recommended_box = models.ForeignKey(
        "boxes.ShippingBox",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="recommendations",
    )
    total_weight = models.DecimalField(max_digits=10, decimal_places=3)
    required_length = models.DecimalField(max_digits=8, decimal_places=2)
    required_width = models.DecimalField(max_digits=8, decimal_places=2)
    required_height = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=RecommendationStatus.choices,
        db_index=True,
    )
    message = models.CharField(max_length=255)
    is_confirmed = models.BooleanField(default=False)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Recommendation for {self.order.order_number}"
