"""URL configuration for shipping boxes."""

from django.urls import path

from boxes.views import ShippingBoxDetailView, ShippingBoxListView

app_name = "boxes"

urlpatterns = [
    path("", ShippingBoxListView.as_view(), name="list"),
    path("<int:pk>/", ShippingBoxDetailView.as_view(), name="detail"),
]
