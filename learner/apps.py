from django.apps import AppConfig

class LearnerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'learner'

    def ready(self):
        # Cette méthode est appelée quand l'application est prête.
        # On importe les signaux ici pour les connecter.
        import learner.signals