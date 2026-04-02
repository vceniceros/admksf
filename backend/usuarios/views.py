"""Views para la app usuarios."""

import json
from json import JSONDecodeError

from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from shared.api_responses import exception_response, success_response

from .auth_service import AuthService
from .services import UsuarioService


@csrf_exempt
@require_http_methods(["POST"])
def registrar_usuario(request):
    """Registra un nuevo usuario administrativo.

    POST: {
        "correo_electronico": "string",
        "contrasena": "string",
        "nombre": "string",
        "apellido": "string",
        "rol": "superusuario|administrador",
        "esta_activo": bool
    }
    """
    try:
        usuario_autenticado = request.usuario_dominio
        UsuarioService.verificar_superusuario(usuario_autenticado)

        datos = json.loads(request.body)
        usuario = UsuarioService.registrar_usuario(datos)
        return success_response(
            {
                "id": usuario.id,
                "correo_electronico": usuario.correo_electronico,
                "nombre": usuario.nombre,
                "apellido": usuario.apellido,
                "esta_activo": usuario.esta_activo,
                "fecha_creacion": usuario.fecha_creacion.isoformat(),
                "rol": usuario.rol.nombre,
            },
            message="Usuario registrado exitosamente",
            status=201,
        )
    except Exception as exc:
        return exception_response(
            exc,
            validation_message="Error de validación al registrar usuario.",
            forbidden_message="Se requiere un usuario con rol superusuario.",
        )


@csrf_exempt
@require_http_methods(["POST"])
def login_usuario(request):
    """Autentica un usuario y retorna un JWT firmado por backend."""

    try:
        datos = json.loads(request.body)
        usuario = UsuarioService.autenticar_usuario(
            datos.get("usuario", ""),
            datos.get("contrasena", ""),
        )

        return success_response(
            AuthService.build_auth_response(
                usuario,
                AuthService.generate_jwt(usuario),
            ),
            message="Login exitoso",
        )
    except Exception as exc:
        return exception_response(
            exc,
            validation_message="Error de validación al iniciar sesión.",
        )


@csrf_exempt
@require_http_methods(["GET"])
def verificar_autenticacion(request):
    """Valida el JWT actual y refresca el token si sigue activo y está próximo a vencer."""

    try:
        usuario = request.usuario_dominio
        token = getattr(request, "jwt_token", None)
        refreshed_token = getattr(request, "jwt_refreshed_token", None)
        response_token = refreshed_token or token

        return success_response(
            AuthService.build_auth_response(
                usuario,
                response_token,
                refreshed=bool(refreshed_token),
            ),
            message="Token válido",
        )
    except Exception as exc:
        if isinstance(exc, ValidationError):
            return exception_response(
                exc,
                validation_message="Error de validación al verificar autenticación.",
                unexpected_message="La sesión no es válida.",
            )
        return exception_response(exc, unexpected_message="La sesión no es válida.")


@csrf_exempt
@require_http_methods(["POST"])
def recuperar_contrasena_usuario(request):
    """Permite a un superusuario resetear manualmente la contraseña de otro usuario."""

    try:
        usuario_autenticado = request.usuario_dominio
        UsuarioService.verificar_superusuario(usuario_autenticado)

        datos = json.loads(request.body)
        usuario_objetivo, password_plano = UsuarioService.recuperar_contrasena(
            datos.get("correo_electronico", ""),
            datos.get("nueva_contrasena"),
        )

        return success_response(
            {
                "id": usuario_objetivo.id,
                "correo_electronico": usuario_objetivo.correo_electronico,
                "rol": usuario_objetivo.rol.nombre,
                "contrasena_temporal": password_plano,
                "generada_automaticamente": "nueva_contrasena" not in datos,
            },
            message="Contraseña reseteada exitosamente",
        )
    except Exception as exc:
        return exception_response(
            exc,
            validation_message="Error de validación al recuperar contraseña.",
        )