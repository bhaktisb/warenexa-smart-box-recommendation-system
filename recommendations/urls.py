"""URL configuration for recommendations."""

from django.urls import path

from recommendations.views import RecommendationDetailView, RecommendationListView

app_name = "recommendations"

urlpatterns = [
    path("", RecommendationListView.as_view(), name="list"),
    path("<int:pk>/", RecommendationDetailView.as_view(), name="detail"),
]
