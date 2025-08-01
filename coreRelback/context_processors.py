from .models import RelbackUser

def relback_user(request):
    """
    Context processor para disponibilizar RelbackUser em todos os templates
    """
    context = {}
    if request.user.is_authenticated:
        try:
            relback_user = RelbackUser.objects.get(username=request.user.username)
            context['relback_user'] = relback_user
        except RelbackUser.DoesNotExist:
            context['relback_user'] = None
    return context
