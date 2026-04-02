"""Views para la app caratula.

Fecha:
    31 - 01 - 2026
"""

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from shared.api_responses import exception_response, success_response
from shared.auth import ensure_consorcio_access, filter_queryset_by_consorcios, get_request_user

from .services import CaratulaService


@csrf_exempt
@require_http_methods(["POST"])
def crear_caratula(request):
    """Crea una nueva carátula.
    
    POST: {
        "fecha_caratula": "datetime",
        "consorcio": "string (cuit)",
        "texto_caratula": "string"
    }
    """
    try:
        usuario_autenticado = get_request_user(request)
        datos = json.loads(request.body)
        if "consorcio" in datos:
            datos["consorcio_id"] = datos.pop("consorcio")
        ensure_consorcio_access(usuario_autenticado, datos.get("consorcio_id"))
        caratula = CaratulaService.crear_caratula(datos)
        return success_response({
            "fecha": caratula.fecha_caratula.isoformat(),
            "consorcio": str(caratula.consorcio.cuit),
        }, message="Carátula creada exitosamente", status=201)
    except Exception as e:
        return exception_response(e, validation_message="Error de validación al crear carátula.")


@csrf_exempt
@require_http_methods(["GET"])
def obtener_caratula(request, fecha_caratula):
    """Obtiene una carátula específica."""
    try:
        usuario_autenticado = get_request_user(request)
        caratula = CaratulaService.obtener_caratula(fecha_caratula)
        ensure_consorcio_access(usuario_autenticado, caratula.consorcio_id)
        return success_response({
            "fecha": caratula.fecha_caratula.isoformat(),
            "consorcio": str(caratula.consorcio.cuit),
            "texto": caratula.texto_caratula,
        })
    except Exception as e:
        return exception_response(e, not_found_message="Carátula no encontrada.")


@csrf_exempt
@require_http_methods(["GET"])
def listar_caratulas(request):
    """Lista todas las carátulas."""
    try:
        usuario_autenticado = get_request_user(request)
        caratulas = filter_queryset_by_consorcios(
            CaratulaService.listar_caratulas(),
            usuario_autenticado,
        )
        datos = [{
            "fecha": c.fecha_caratula.isoformat(),
            "consorcio": str(c.consorcio.cuit),
            "texto_preview": c.texto_caratula[:100],
        } for c in caratulas]
        return success_response(datos, count=len(datos))
    except Exception as e:
        return exception_response(e)


@csrf_exempt
@require_http_methods(["GET"])
def listar_caratulas_por_consorcio(request, cuit_consorcio):
    """Lista carátulas de un consorcio."""
    try:
        usuario_autenticado = get_request_user(request)
        ensure_consorcio_access(usuario_autenticado, cuit_consorcio)
        caratulas = CaratulaService.listar_caratulas_por_consorcio(cuit_consorcio)
        datos = [{
            "fecha": c.fecha_caratula.isoformat(),
            "consorcio": str(c.consorcio.cuit),
            "texto": c.texto_caratula,
            "texto_preview": c.texto_caratula[:100],
        } for c in caratulas]
        return success_response(datos, count=len(datos))
    except Exception as e:
        return exception_response(e)


@csrf_exempt
@require_http_methods(["PUT"])
def actualizar_caratula(request, fecha_caratula):
    """Actualiza una carátula existente."""
    try:
        usuario_autenticado = get_request_user(request)
        datos = json.loads(request.body)
        caratula_actual = CaratulaService.obtener_caratula(fecha_caratula)
        ensure_consorcio_access(usuario_autenticado, caratula_actual.consorcio_id)
        if "consorcio" in datos:
            datos["consorcio_id"] = datos.pop("consorcio")
        if "consorcio_id" in datos:
            ensure_consorcio_access(usuario_autenticado, datos.get("consorcio_id"))
        caratula = CaratulaService.actualizar_caratula(fecha_caratula, datos)
        return success_response({
            "fecha": caratula.fecha_caratula.isoformat(),
            "consorcio": str(caratula.consorcio.cuit),
        }, message="Carátula actualizada exitosamente")
    except Exception as e:
        return exception_response(
            e,
            validation_message="Error de validación al actualizar carátula.",
            not_found_message="Carátula no encontrada.",
        )


@csrf_exempt
@require_http_methods(["DELETE"])
def eliminar_caratula(request, fecha_caratula):
    """Elimina una carátula."""
    try:
        usuario_autenticado = get_request_user(request)
        caratula = CaratulaService.obtener_caratula(fecha_caratula)
        ensure_consorcio_access(usuario_autenticado, caratula.consorcio_id)
        CaratulaService.eliminar_caratula(fecha_caratula)
        return success_response(message="Carátula eliminada exitosamente")
    except Exception as e:
        return exception_response(e, not_found_message="Carátula no encontrada.")
