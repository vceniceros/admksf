"""Views para la app usuarios."""

import json
from json import JSONDecodeError

from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

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
        datos = json.loads(request.body)
        usuario = UsuarioService.registrar_usuario(datos)
        return JsonResponse(
            {
                "status": "success",
                "message": "Usuario registrado exitosamente",
                "data": {
                    "id": usuario.id,
                    "correo_electronico": usuario.correo_electronico,
                    "nombre": usuario.nombre,
                    "apellido": usuario.apellido,
                    "esta_activo": usuario.esta_activo,
                    "fecha_creacion": usuario.fecha_creacion.isoformat(),
                    "rol": usuario.rol.nombre,
                },
            },
            status=201,
        )
    except JSONDecodeError:
        return JsonResponse(
            {
                "status": "error",
                "message": "JSON inválido en el cuerpo de la solicitud.",
                "errors": {"body": ["No se pudo interpretar el JSON enviado."]},
            },
            status=400,
        )
    except ValidationError as exc:
        error_details = exc.message_dict if hasattr(exc, "message_dict") else {"non_field_errors": exc.messages}
        return JsonResponse(
            {
                "status": "error",
                "message": "Error de validación al registrar usuario.",
                "errors": error_details,
            },
            status=400,
        )
    except Exception as exc:
        return JsonResponse(
            {
                "status": "error",
                "message": str(exc),
            },
            status=500,
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

        return JsonResponse(
            {
                "status": "success",
                "message": "Login exitoso",
                "data": AuthService.build_auth_response(
                    usuario,
                    AuthService.generate_jwt(usuario),
                ),
            }
        )
    except JSONDecodeError:
        return JsonResponse(
            {
                "status": "error",
                "message": "JSON inválido en el cuerpo de la solicitud.",
                "errors": {"body": ["No se pudo interpretar el JSON enviado."]},
            },
            status=400,
        )
    except ValidationError as exc:
        error_details = exc.message_dict if hasattr(exc, "message_dict") else {"non_field_errors": exc.messages}
        return JsonResponse(
            {
                "status": "error",
                "message": "Error de validación al iniciar sesión.",
                "errors": error_details,
            },
            status=400,
        )
    except Exception as exc:
        return JsonResponse(
            {
                "status": "error",
                "message": str(exc),
            },
            status=500,
        )


@csrf_exempt
@require_http_methods(["GET"])
def verificar_autenticacion(request):
    """Valida el JWT actual y refresca el token si sigue activo y está próximo a vencer."""

    try:
        token = AuthService.extract_bearer_token(request.headers.get("Authorization"))
        usuario, refreshed_token = UsuarioService.validar_sesion(token)
        response_token = refreshed_token or token

        return JsonResponse(
            {
                "status": "success",
                "message": "Token válido",
                "data": AuthService.build_auth_response(
                    usuario,
                    response_token,
                    refreshed=bool(refreshed_token),
                ),
            }
        )
    except ValidationError as exc:
        error_details = exc.message_dict if hasattr(exc, "message_dict") else {"non_field_errors": exc.messages}
        return JsonResponse(
            {
                "status": "error",
                "message": "Error de validación al verificar autenticación.",
                "errors": error_details,
            },
            status=401,
        )
    except Exception as exc:
        return JsonResponse(
            {
                "status": "error",
                "message": str(exc),
            },
            status=500,
        )


@csrf_exempt
@require_http_methods(["POST"])
def recuperar_contrasena_usuario(request):
    """Permite a un superusuario resetear manualmente la contraseña de otro usuario."""

    try:
        token = AuthService.extract_bearer_token(request.headers.get("Authorization"))
        usuario_autenticado, _ = UsuarioService.validar_sesion(token)
        UsuarioService.verificar_superusuario(usuario_autenticado)

        datos = json.loads(request.body)
        usuario_objetivo, password_plano = UsuarioService.recuperar_contrasena(
            datos.get("correo_electronico", ""),
            datos.get("nueva_contrasena"),
        )

        return JsonResponse(
            {
                "status": "success",
                "message": "Contraseña reseteada exitosamente",
                "data": {
                    "id": usuario_objetivo.id,
                    "correo_electronico": usuario_objetivo.correo_electronico,
                    "rol": usuario_objetivo.rol.nombre,
                    "contrasena_temporal": password_plano,
                    "generada_automaticamente": "nueva_contrasena" not in datos,
                },
            }
        )
    except JSONDecodeError:
        return JsonResponse(
            {
                "status": "error",
                "message": "JSON inválido en el cuerpo de la solicitud.",
                "errors": {"body": ["No se pudo interpretar el JSON enviado."]},
            },
            status=400,
        )
    except PermissionDenied as exc:
        return JsonResponse(
            {
                "status": "error",
                "message": str(exc),
            },
            status=403,
        )
    except ValidationError as exc:
        error_details = exc.message_dict if hasattr(exc, "message_dict") else {"non_field_errors": exc.messages}
        return JsonResponse(
            {
                "status": "error",
                "message": "Error de validación al recuperar contraseña.",
                "errors": error_details,
            },
            status=400,
        )
    except Exception as exc:
        return JsonResponse(
            {
                "status": "error",
                "message": str(exc),
            },
            status=500,
        )