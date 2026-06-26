"""Reusable view mixins for the warehouse application."""

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Restrict warehouse views to authenticated staff users."""

    def test_func(self) -> bool:
        return self.request.user.is_staff

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            from django.core.exceptions import PermissionDenied

            raise PermissionDenied
        return super().handle_no_permission()
