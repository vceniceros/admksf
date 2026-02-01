"""Views para la app reparaciones_mantenimientos.

Fecha:
    31 - 01 - 2026
"""

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

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
        return JsonResponse({
            "status": "success",
            "message": "Reparación/Mantenimiento creado exitosamente",
            "data": {
                "cuit": str(rm.proveedor.cuit),
                "numero_reclamo": rm.numero_reclamo,
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
def obtener_reparacion_mantenimiento(request, cuit_proveedor):
    """Obtiene un registro de reparación/mantenimiento específico."""
    try:
        rm = ReparacionMantenimientoService.obtener_reparacion_mantenimiento(cuit_proveedor)
        return JsonResponse({
            "status": "success",
            "data": {
                "cuit": str(rm.proveedor.cuit),
                "razon_social": rm.proveedor.razon_social,
                "numero_reclamo": rm.numero_reclamo,
            }
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": f"Reparación/Mantenimiento no encontrado: {str(e)}",
        }, status=404)


@csrf_exempt
@require_http_methods(["GET"])
def listar_reparaciones_mantenimientos(request):
    """Lista todos los registros de reparación/mantenimiento."""
    try:
        rms = ReparacionMantenimientoService.listar_reparaciones_mantenimientos()
        datos = [{
            "cuit": str(rm.proveedor.cuit),
            "razon_social": rm.proveedor.razon_social,
            "numero_reclamo": rm.numero_reclamo,
        } for rm in rms]
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
def actualizar_reparacion_mantenimiento(request, cuit_proveedor):
    """Actualiza un registro de reparación/mantenimiento existente."""
    try:
        datos = json.loads(request.body)
        if "proveedor" in datos:
            datos["proveedor_id"] = datos.pop("proveedor")
        rm = ReparacionMantenimientoService.actualizar_reparacion_mantenimiento(cuit_proveedor, datos)
        return JsonResponse({
            "status": "success",
            "message": "Reparación/Mantenimiento actualizado exitosamente",
            "data": {
                "cuit": str(rm.proveedor.cuit),
                "numero_reclamo": rm.numero_reclamo,
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
def eliminar_reparacion_mantenimiento(request, cuit_proveedor):
    """Elimina un registro de reparación/mantenimiento."""
    try:
        ReparacionMantenimientoService.eliminar_reparacion_mantenimiento(cuit_proveedor)
        return JsonResponse({
            "status": "success",
            "message": "Reparación/Mantenimiento eliminado exitosamente",
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e),
        }, status=404)
