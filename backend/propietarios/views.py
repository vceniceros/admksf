"""Views para la app propietarios.

Fecha:
    31 - 01 - 2026
"""

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

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
        return JsonResponse({
            "status": "success",
            "message": "Propietario creado exitosamente",
            "data": {
                "dni": str(propietario.dni),
                "nombre": propietario.nombre,
                "apellido": propietario.apellido,
            }
        }, status=201)
    except ValidationError as e:
        return JsonResponse({
            "status": "error",
            "message": str(e.messages),
        }, status=400)
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e),
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def obtener_propietario(request, dni):
    """Obtiene un propietario específico."""
    try:
        propietario = PropietarioService.obtener_propietario(dni)
        return JsonResponse({
            "status": "success",
            "data": {
                "dni": str(propietario.dni),
                "nombre": propietario.nombre,
                "apellido": propietario.apellido,
                "telefono": propietario.telefono,
                "email": propietario.email,
            }
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": f"Propietario no encontrado: {str(e)}",
        }, status=404)


@csrf_exempt
@require_http_methods(["GET"])
def listar_propietarios(request):
    """Lista todos los propietarios."""
    try:
        propietarios = PropietarioService.listar_propietarios()
        datos = [{
            "dni": str(p.dni),
            "nombre": p.nombre,
            "apellido": p.apellido,
            "telefono": p.telefono,
            "email": p.email,
        } for p in propietarios]
        return JsonResponse({
            "status": "success",
            "count": len(datos),
            "data": datos
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e),
        }, status=500)


@csrf_exempt
@require_http_methods(["PUT"])
def actualizar_propietario(request, dni):
    """Actualiza un propietario existente."""
    try:
        datos = json.loads(request.body)
        propietario = PropietarioService.actualizar_propietario(dni, datos)
        return JsonResponse({
            "status": "success",
            "message": "Propietario actualizado exitosamente",
            "data": {
                "dni": str(propietario.dni),
                "nombre": propietario.nombre,
                "apellido": propietario.apellido,
            }
        })
    except ValidationError as e:
        return JsonResponse({
            "status": "error",
            "message": str(e.messages),
        }, status=400)
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e),
        }, status=404)


@csrf_exempt
@require_http_methods(["DELETE"])
def eliminar_propietario(request, dni):
    """Elimina un propietario."""
    try:
        PropietarioService.eliminar_propietario(dni)
        return JsonResponse({
            "status": "success",
            "message": "Propietario eliminado exitosamente",
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e),
        }, status=404)
