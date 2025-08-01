# Settings para desenvolvimento sem banco de dados
from .settings import *

# Desabilitar verificações de banco para desenvolvimento
DATABASES = {}

# Usar cache dummy
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Desabilitar migrações automáticas
class DisableMigrations:
    def __contains__(self, item):
        return True
    
    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()

# Para desenvolvimento: permitir templates sem contexto
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG
