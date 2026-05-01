from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

class RoleRequiredMixin(UserPassesTestMixin):
    allowed_roles = None

    def test_func(self):
        if not self.allowed_roles:
            return True

        return self.request.user.profile.roles.filter(
            name__in=self.allowed_roles
        ).exists()

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        raise PermissionDenied