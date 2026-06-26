"""URL configuration for orders."""

from django.urls import path

from orders.views import (
    ConfirmPackingView,
    OrderDetailView,
    OrderListView,
    RecommendBoxView,
)

app_name = "orders"

urlpatterns = [
    path("", OrderListView.as_view(), name="list"),
    path("<int:pk>/", OrderDetailView.as_view(), name="detail"),
    path("<int:pk>/recommend/", RecommendBoxView.as_view(), name="recommend"),
    path("<int:pk>/confirm-packing/", ConfirmPackingView.as_view(), name="confirm_packing"),
]
