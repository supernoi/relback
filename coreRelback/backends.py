from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from .models import RelbackUser

class RelbackUserBackend(BaseBackend):
    """
    Backend de autenticação customizado para RelbackUser
    Autentica usando RelbackUser mas cria/usa User do Django para sessões
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Buscar usuário RelbackUser
            relback_user = RelbackUser.objects.get(username=username)
            if relback_user.check_password(password) and relback_user.status == 1:
                # Criar ou obter User do Django correspondente
                django_user, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        'email': relback_user.email or '',
                        'first_name': relback_user.name or '',
                        'is_active': True,
                    }
                )
                
                # Atualizar last_login no RelbackUser
                from django.utils import timezone
                relback_user.last_login = timezone.now()
                relback_user.save()
                
                # Adicionar referência ao RelbackUser no User do Django
                django_user.relback_user = relback_user
                
                return django_user
        except RelbackUser.DoesNotExist:
            return None
        return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
