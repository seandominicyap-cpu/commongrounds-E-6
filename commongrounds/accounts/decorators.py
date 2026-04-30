from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def role_required(allowed_roles):
    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return login_required(view_func)(request, *args, **kwargs)

            user_roles = request.user.profile.roles.filter(
                name__in=allowed_roles
            ).exists()

            if not user_roles:
                raise PermissionDenied

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator