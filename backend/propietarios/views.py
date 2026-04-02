"""Views para la app propietarios.

Fecha:
    31 - 01 - 2026
"""

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from shared.api_responses import exception_response, success_response
from shared.auth import ensure_propietario_access, filter_propietarios_queryset, get_request_user

from .services import PropietarioService


@csrf_exempt
@require_http_methods(["POST"])
def crear_propietario(request):
    """Crea un nuevo propietario.
    
    POST: {
        "dni": "string",
        "nombre": "string",
        "apellido": "string",
        "telefono": "string (optional)",
        "email": "string (optional)"
    }
    """
    try:
        datos = json.loads(request.body)
        propietario = PropietarioService.crear_propietario(datos)
        return success_response({
            "dni": str(propietario.dni),
            "nombre": propietario.nombre,
            "apellido": propietario.apellido,
        }, message="Propietario creado exitosamente", status=201)
    except Exception as e:
        return exception_response(e, validation_message="Error de validación al crear propietario.")


@csrf_exempt
@require_http_methods(["GET"])
def obtener_propietario(request, dni):
    """Obtiene un propietario específico."""
    try:
        usuario_autenticado = get_request_user(request)
        propietario = ensure_propietario_access(
            PropietarioService.listar_propietarios(),
            usuario_autenticado,
            dni,
        )
        return success_response({
            "dni": str(propietario.dni),
            "nombre": propietario.nombre,
            "apellido": propietario.apellido,
            "telefono": propietario.telefono,
            "email": propietario.email,
        })
    except Exception as e:
        return exception_response(e, not_found_message="Propietario no encontrado.")


@csrf_exempt
@require_http_methods(["GET"])
def listar_propietarios(request):
    """Lista todos los propietarios."""
    try:
        usuario_autenticado = get_request_user(request)
        propietarios = filter_propietarios_queryset(
            PropietarioService.listar_propietarios(),
            usuario_autenticado,
        )
        datos = [{
            "dni": str(p.dni),
            "nombre": p.nombre,
            "apellido": p.apellido,
            "telefono": p.telefono,
            "email": p.email,
        } for p in propietarios]
        return success_response(datos, count=len(datos))
    except Exception as e:
        return exception_response(e)


@csrf_exempt
@require_http_methods(["PUT"])
def actualizar_propietario(request, dni):
    """Actualiza un propietario existente."""
    try:
        usuario_autenticado = get_request_user(request)
        ensure_propietario_access(
            PropietarioService.listar_propietarios(),
            usuario_autenticado,
            dni,
        )
        datos = json.loads(request.body)
        propietario = PropietarioService.actualizar_propietario(dni, datos)
        return success_response({
            "dni": str(propietario.dni),
            "nombre": propietario.nombre,
            "apellido": propietario.apellido,
        }, message="Propietario actualizado exitosamente")
    except Exception as e:
        return exception_response(
            e,
            validation_message="Error de validación al actualizar propietario.",
            not_found_message="Propietario no encontrado.",
        )


@csrf_exempt
@require_http_methods(["DELETE"])
def eliminar_propietario(request, dni):
    """Elimina un propietario."""
    try:
        usuario_autenticado = get_request_user(request)
        ensure_propietario_access(
            PropietarioService.listar_propietarios(),
            usuario_autenticado,
            dni,
        )
        PropietarioService.eliminar_propietario(dni)
        return success_response(message="Propietario eliminado exitosamente")
    except Exception as e:
        return exception_response(e, not_found_message="Propietario no encontrado.")
