"""Project URL configuration."""

from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path

admin.site.site_header = "WareNexa Warehouse Suite Admin"
admin.site.site_title = "WareNexa Warehouse Suite"
admin.site.index_title = "Warehouse Operations Administration"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "accounts/login/",
        LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("accounts/logout/", LogoutView.as_view(), name="logout"),
    path("", include("core.urls")),
    path("products/", include("products.urls")),
    path("boxes/", include("boxes.urls")),
    path("orders/", include("orders.urls")),
    path("recommendations/", include("recommendations.urls")),
]
