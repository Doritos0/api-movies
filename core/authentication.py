from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions

class CookieJWTAuthentication(JWTAuthentication):
    """
    Extiende JWTAuthentication para admitir tokens enviados en la cookie 'access'.
    Primero intenta leer el header Authorization; si no existe, busca la cookie.
    """
    def authenticate(self, request):
        # intenta usar el header Authorization primero (comportamiento por defecto)
        header = self.get_header(request)
        if header is not None:
            return super().authenticate(request)

        # si no hay header, buscar la cookie 'access'
        raw_token = request.COOKIES.get('access')
        if raw_token is None:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
            user = self.get_user(validated_token)
            return (user, validated_token)
        except Exception as e:
            # devuelve None para que DRF piense que no hay credenciales válidas;
            # las vistas recibirán 401 y el frontend podrá pedir refresh.
            raise exceptions.AuthenticationFailed("Token inválido/expirado")