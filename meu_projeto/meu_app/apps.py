from django.apps import AppConfig

class MeuAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'meu_app'

    def ready(self):
        import meu_app.filters  # Importe o módulo de filtros quando o aplicativo estiver pronto