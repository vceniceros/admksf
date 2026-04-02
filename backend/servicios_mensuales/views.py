"""Views para la app servicios_mensuales.

Fecha:
    31 - 01 - 2026
"""

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from shared.api_responses import exception_response, success_response
from shared.auth import ensure_proveedor_access, filter_proveedores_queryset, get_request_user

from .services import ServicioMensualService


@csrf_exempt
@require_http_methods(["POST"])
def crear_servicio_mensual(request):
    """Crea un nuevo servicio mensual.
    
    POST: {
        "proveedor": "string (cuit)",
        "numero_cuenta": "string",
        "numero_reclamo": "string"
    }
    """
    try:
        datos = json.loads(request.body)
        if "proveedor" in datos:
            datos["proveedor_id"] = datos.pop("proveedor")
        sm = ServicioMensualService.crear_servicio_mensual(datos)
        return success_response({
            "cuit": str(sm.proveedor.cuit),
            "numero_cuenta": sm.numero_cuenta,
        }, message="Servicio mensual creado exitosamente", status=201)
    except Exception as e:
        return exception_response(e, validation_message="Error de validación al crear servicio mensual.")


@csrf_exempt
@require_http_methods(["GET"])
def obtener_servicio_mensual(request, cuit_proveedor):
    """Obtiene un servicio mensual específico."""
    try:
        usuario_autenticado = get_request_user(request)
        ensure_proveedor_access(
            ServicioMensualService.listar_servicios_mensuales(),
            usuario_autenticado,
            cuit_proveedor,
        )
        sm = ServicioMensualService.obtener_servicio_mensual(cuit_proveedor)
        return success_response({
            "cuit": str(sm.proveedor.cuit),
            "razon_social": sm.proveedor.razon_social,
            "numero_cuenta": sm.numero_cuenta,
            "numero_reclamo": sm.numero_reclamo,
        })
    except Exception as e:
        return exception_response(e, not_found_message="Servicio mensual no encontrado.")


@csrf_exempt
@require_http_methods(["GET"])
def listar_servicios_mensuales(request):
    """Lista todos los servicios mensuales."""
    try:
        usuario_autenticado = get_request_user(request)
        sms = filter_proveedores_queryset(
            ServicioMensualService.listar_servicios_mensuales(),
            usuario_autenticado,
            field_name="proveedor__gasto__consorcio_id",
        )
        datos = [{
            "cuit": str(sm.proveedor.cuit),
            "razon_social": sm.proveedor.razon_social,
            "numero_cuenta": sm.numero_cuenta,
            "numero_reclamo": sm.numero_reclamo,
        } for sm in sms]
        return success_response(datos, count=len(datos))
    except Exception as e:
        return exception_response(e)


@csrf_exempt
@require_http_methods(["PUT"])
def actualizar_servicio_mensual(request, cuit_proveedor):
    """Actualiza un servicio mensual existente."""
    try:
        usuario_autenticado = get_request_user(request)
        ensure_proveedor_access(
            ServicioMensualService.listar_servicios_mensuales(),
            usuario_autenticado,
            cuit_proveedor,
        )
        datos = json.loads(request.body)
        if "proveedor" in datos:
            datos["proveedor_id"] = datos.pop("proveedor")
            ensure_proveedor_access(
                ServicioMensualService.listar_servicios_mensuales(),
                usuario_autenticado,
                datos["proveedor_id"],
            )
        sm = ServicioMensualService.actualizar_servicio_mensual(cuit_proveedor, datos)
        return success_response({
            "cuit": str(sm.proveedor.cuit),
            "numero_cuenta": sm.numero_cuenta,
        }, message="Servicio mensual actualizado exitosamente")
    except Exception as e:
        return exception_response(
            e,
            validation_message="Error de validación al actualizar servicio mensual.",
            not_found_message="Servicio mensual no encontrado.",
        )


@csrf_exempt
@require_http_methods(["DELETE"])
def eliminar_servicio_mensual(request, cuit_proveedor):
    """Elimina un servicio mensual."""
    try:
        usuario_autenticado = get_request_user(request)
        ensure_proveedor_access(
            ServicioMensualService.listar_servicios_mensuales(),
            usuario_autenticado,
            cuit_proveedor,
        )
        ServicioMensualService.eliminar_servicio_mensual(cuit_proveedor)
        return success_response(message="Servicio mensual eliminado exitosamente")
    except Exception as e:
        return exception_response(e, not_found_message="Servicio mensual no encontrado.")
