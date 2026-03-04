from .models import RelbackUser

def relback_user(request):
    """
    Context processor: RelbackUser + role flags for templates (Phase 16).
    """
    context = {}
    if request.user.is_authenticated:
        try:
            ru = RelbackUser.objects.get(username=request.user.username)
            context["relback_user"] = ru
            context["user_role"] = ru.role
            context["user_can_edit"] = ru.role in (RelbackUser.ROLE_ADMIN, RelbackUser.ROLE_OPERATOR)
            context["user_can_delete"] = ru.role == RelbackUser.ROLE_ADMIN
        except RelbackUser.DoesNotExist:
            context["relback_user"] = None
            context["user_role"] = None
            context["user_can_edit"] = False
            context["user_can_delete"] = False
    return context
