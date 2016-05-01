from django.apps import AppConfig
from django.db.models.fields import CharField
from django.db.models.fields import TextField

from .lookups import Similar


class PgTrgmConfig(AppConfig):
    name = 'pg_trgm'

    def ready(self):
        CharField.register_lookup(Similar)
        TextField.register_lookup(Similar)
