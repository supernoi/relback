"""
View mixins for Relback.

RoleRequiredMixin: restricts access by RelbackUser.role (admin / operator / viewer).
"""
from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseForbidden

from .models import RelbackUser


def get_relback_user_role(request):
    """Return the role of the current user's RelbackUser, or 'operator' if no profile (backward compatibility)."""
    if not getattr(request, "user", None) or not request.user.is_authenticated:
        return None
    try:
        relback_user = RelbackUser.objects.get(username=request.user.username)
        return relback_user.role
    except RelbackUser.DoesNotExist:
        return RelbackUser.ROLE_OPERATOR  # legacy: no profile => treat as operator
    except Exception:
        return None


class RoleRequiredMixin(AccessMixin):
    """
    CBV mixin: allow access only if the current user's RelbackUser.role is in required_roles.

    Use as: class MyDeleteView(RoleRequiredMixin, DeleteView): required_roles = ['admin']
    If the user has no RelbackUser or role not in required_roles, returns 403.
    """

    required_roles = None  # e.g. ['admin'] or ['admin', 'operator']

    def dispatch(self, request, *args, **kwargs):
        if self.required_roles is None:
            return super().dispatch(request, *args, **kwargs)
        role = get_relback_user_role(request)
        if role not in self.required_roles:
            return HttpResponseForbidden(
                "You do not have permission to perform this action."
            )
        return super().dispatch(request, *args, **kwargs)
