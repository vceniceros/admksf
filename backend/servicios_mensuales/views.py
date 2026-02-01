"""Views para la app servicios_mensuales.

Fecha:
    31 - 01 - 2026
"""

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

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
        return JsonResponse({
            "status": "success",
            "message": "Servicio mensual creado exitosamente",
            "data": {
                "cuit": str(sm.proveedor.cuit),
                "numero_cuenta": sm.numero_cuenta,
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
def obtener_servicio_mensual(request, cuit_proveedor):
    """Obtiene un servicio mensual específico."""
    try:
        sm = ServicioMensualService.obtener_servicio_mensual(cuit_proveedor)
        return JsonResponse({
            "status": "success",
            "data": {
                "cuit": str(sm.proveedor.cuit),
                "razon_social": sm.proveedor.razon_social,
                "numero_cuenta": sm.numero_cuenta,
                "numero_reclamo": sm.numero_reclamo,
            }
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": f"Servicio mensual no encontrado: {str(e)}",
        }, status=404)


@csrf_exempt
@require_http_methods(["GET"])
def listar_servicios_mensuales(request):
    """Lista todos los servicios mensuales."""
    try:
        sms = ServicioMensualService.listar_servicios_mensuales()
        datos = [{
            "cuit": str(sm.proveedor.cuit),
            "razon_social": sm.proveedor.razon_social,
            "numero_cuenta": sm.numero_cuenta,
            "numero_reclamo": sm.numero_reclamo,
        } for sm in sms]
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
def actualizar_servicio_mensual(request, cuit_proveedor):
    """Actualiza un servicio mensual existente."""
    try:
        datos = json.loads(request.body)
        if "proveedor" in datos:
            datos["proveedor_id"] = datos.pop("proveedor")
        sm = ServicioMensualService.actualizar_servicio_mensual(cuit_proveedor, datos)
        return JsonResponse({
            "status": "success",
            "message": "Servicio mensual actualizado exitosamente",
            "data": {
                "cuit": str(sm.proveedor.cuit),
                "numero_cuenta": sm.numero_cuenta,
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
def eliminar_servicio_mensual(request, cuit_proveedor):
    """Elimina un servicio mensual."""
    try:
        ServicioMensualService.eliminar_servicio_mensual(cuit_proveedor)
        return JsonResponse({
            "status": "success",
            "message": "Servicio mensual eliminado exitosamente",
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e),
        }, status=404)
