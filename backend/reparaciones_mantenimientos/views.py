"""Views para la app reparaciones_mantenimientos.

Fecha:
    31 - 01 - 2026
"""

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from shared.api_responses import exception_response, success_response
from shared.auth import ensure_proveedor_access, filter_proveedores_queryset, get_request_user

from .services import ReparacionMantenimientoService


@csrf_exempt
@require_http_methods(["POST"])
def crear_reparacion_mantenimiento(request):
    """Crea un nuevo registro de reparación/mantenimiento.
    
    POST: {
        "proveedor": "string (cuit)",
        "numero_reclamo": "string"
    }
    """
    try:
        datos = json.loads(request.body)
        if "proveedor" in datos:
            datos["proveedor_id"] = datos.pop("proveedor")
        rm = ReparacionMantenimientoService.crear_reparacion_mantenimiento(datos)
        return success_response({
            "cuit": str(rm.proveedor.cuit),
            "numero_reclamo": rm.numero_reclamo,
        }, message="Reparación/Mantenimiento creado exitosamente", status=201)
    except Exception as e:
        return exception_response(e, validation_message="Error de validación al crear reparación o mantenimiento.")


@csrf_exempt
@require_http_methods(["GET"])
def obtener_reparacion_mantenimiento(request, cuit_proveedor):
    """Obtiene un registro de reparación/mantenimiento específico."""
    try:
        usuario_autenticado = get_request_user(request)
        ensure_proveedor_access(
            ReparacionMantenimientoService.listar_reparaciones_mantenimientos(),
            usuario_autenticado,
            cuit_proveedor,
        )
        rm = ReparacionMantenimientoService.obtener_reparacion_mantenimiento(cuit_proveedor)
        return success_response({
            "cuit": str(rm.proveedor.cuit),
            "razon_social": rm.proveedor.razon_social,
            "numero_reclamo": rm.numero_reclamo,
        })
    except Exception as e:
        return exception_response(e, not_found_message="Reparación/Mantenimiento no encontrado.")


@csrf_exempt
@require_http_methods(["GET"])
def listar_reparaciones_mantenimientos(request):
    """Lista todos los registros de reparación/mantenimiento."""
    try:
        usuario_autenticado = get_request_user(request)
        rms = filter_proveedores_queryset(
            ReparacionMantenimientoService.listar_reparaciones_mantenimientos(),
            usuario_autenticado,
            field_name="proveedor__gasto__consorcio_id",
        )
        datos = [{
            "cuit": str(rm.proveedor.cuit),
            "razon_social": rm.proveedor.razon_social,
            "numero_reclamo": rm.numero_reclamo,
        } for rm in rms]
        return success_response(datos, count=len(datos))
    except Exception as e:
        return exception_response(e)


@csrf_exempt
@require_http_methods(["PUT"])
def actualizar_reparacion_mantenimiento(request, cuit_proveedor):
    """Actualiza un registro de reparación/mantenimiento existente."""
    try:
        usuario_autenticado = get_request_user(request)
        ensure_proveedor_access(
            ReparacionMantenimientoService.listar_reparaciones_mantenimientos(),
            usuario_autenticado,
            cuit_proveedor,
        )
        datos = json.loads(request.body)
        if "proveedor" in datos:
            datos["proveedor_id"] = datos.pop("proveedor")
            ensure_proveedor_access(
                ReparacionMantenimientoService.listar_reparaciones_mantenimientos(),
                usuario_autenticado,
                datos["proveedor_id"],
            )
        rm = ReparacionMantenimientoService.actualizar_reparacion_mantenimiento(cuit_proveedor, datos)
        return success_response({
            "cuit": str(rm.proveedor.cuit),
            "numero_reclamo": rm.numero_reclamo,
        }, message="Reparación/Mantenimiento actualizado exitosamente")
    except Exception as e:
        return exception_response(
            e,
            validation_message="Error de validación al actualizar reparación o mantenimiento.",
            not_found_message="Reparación/Mantenimiento no encontrado.",
        )


@csrf_exempt
@require_http_methods(["DELETE"])
def eliminar_reparacion_mantenimiento(request, cuit_proveedor):
    """Elimina un registro de reparación/mantenimiento."""
    try:
        usuario_autenticado = get_request_user(request)
        ensure_proveedor_access(
            ReparacionMantenimientoService.listar_reparaciones_mantenimientos(),
            usuario_autenticado,
            cuit_proveedor,
        )
        ReparacionMantenimientoService.eliminar_reparacion_mantenimiento(cuit_proveedor)
        return success_response(message="Reparación/Mantenimiento eliminado exitosamente")
    except Exception as e:
        return exception_response(e, not_found_message="Reparación/Mantenimiento no encontrado.")
