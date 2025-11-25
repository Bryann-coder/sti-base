from rest_framework.authentication import SessionAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    Authentification par session standard, mais sans la vérification CSRF.
    Idéal pour les APIs testées via Postman ou Mobile.
    """
    def enforce_csrf(self, request):
        # On ne fait rien ici, ce qui désactive la vérification CSRF
        return None