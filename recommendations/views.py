"""Presentation layer views for recommendation history."""

from django.views.generic import DetailView, ListView

from core.mixins import StaffRequiredMixin
from recommendations.models import BoxRecommendation


class RecommendationListView(StaffRequiredMixin, ListView):
    """List historical box recommendations."""

    model = BoxRecommendation
    template_name = "recommendations/recommendation_list.html"
    context_object_name = "recommendations"
    paginate_by = 20
    ordering = ["-created_at"]

    def get_queryset(self):
        return BoxRecommendation.objects.select_related("order", "recommended_box")


class RecommendationDetailView(StaffRequiredMixin, DetailView):
    """Display recommendation details."""

    model = BoxRecommendation
    template_name = "recommendations/recommendation_detail.html"
    context_object_name = "recommendation"

    def get_queryset(self):
        return BoxRecommendation.objects.select_related("order", "recommended_box")
