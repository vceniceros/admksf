"""Middleware JWT global para la API."""

from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError

from shared.api_responses import error_response
from usuarios.auth_service import AuthService
from usuarios.services import UsuarioService


class JWTAuthenticationMiddleware:
    """Protege la API con JWT, dejando abierto solo el login."""

    EXEMPT_PATHS = {
        "/api/usuarios/login/",
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self._requires_authentication(request):
            try:
                token = AuthService.extract_bearer_token(request.headers.get("Authorization"))
                usuario, refreshed_token = UsuarioService.validar_sesion(token)
                request.usuario_dominio = usuario
                request.jwt_token = token
                request.jwt_refreshed_token = refreshed_token
            except ValidationError as exc:
                error_details = exc.message_dict if hasattr(exc, "message_dict") else {"non_field_errors": exc.messages}
                return error_response(
                    "Autenticación requerida o inválida.",
                    401,
                    errors=error_details,
                )

        try:
            return self.get_response(request)
        except PermissionDenied as exc:
            return error_response(str(exc), 403)

    def _requires_authentication(self, request) -> bool:
        if request.method == "OPTIONS":
            return False

        if not request.path.startswith("/api/"):
            return False

        return request.path not in self.EXEMPT_PATHS