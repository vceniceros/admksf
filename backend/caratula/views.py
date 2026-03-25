"""Views para la app caratula.

Fecha:
    31 - 01 - 2026
"""

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

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
        datos = json.loads(request.body)
        if "consorcio" in datos:
            datos["consorcio_id"] = datos.pop("consorcio")
        caratula = CaratulaService.crear_caratula(datos)
        return JsonResponse({
            "status": "success",
            "message": "Carátula creada exitosamente",
            "data": {
                "fecha": caratula.fecha_caratula.isoformat(),
                "consorcio": str(caratula.consorcio.cuit),
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
def obtener_caratula(request, fecha_caratula):
    """Obtiene una carátula específica."""
    try:
        caratula = CaratulaService.obtener_caratula(fecha_caratula)
        return JsonResponse({
            "status": "success",
            "data": {
                "fecha": caratula.fecha_caratula.isoformat(),
                "consorcio": str(caratula.consorcio.cuit),
                "texto": caratula.texto_caratula,
            }
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": f"Carátula no encontrada: {str(e)}",
        }, status=404)


@csrf_exempt
@require_http_methods(["GET"])
def listar_caratulas(request):
    """Lista todas las carátulas."""
    try:
        caratulas = CaratulaService.listar_caratulas()
        datos = [{
            "fecha": c.fecha_caratula.isoformat(),
            "consorcio": str(c.consorcio.cuit),
            "texto_preview": c.texto_caratula[:100],
        } for c in caratulas]
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
@require_http_methods(["GET"])
def listar_caratulas_por_consorcio(request, cuit_consorcio):
    """Lista carátulas de un consorcio."""
    try:
        caratulas = CaratulaService.listar_caratulas_por_consorcio(cuit_consorcio)
        datos = [{
            "fecha": c.fecha_caratula.isoformat(),
            "consorcio": str(c.consorcio.cuit),
            "texto": c.texto_caratula,
            "texto_preview": c.texto_caratula[:100],
        } for c in caratulas]
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
def actualizar_caratula(request, fecha_caratula):
    """Actualiza una carátula existente."""
    try:
        datos = json.loads(request.body)
        if "consorcio" in datos:
            datos["consorcio_id"] = datos.pop("consorcio")
        caratula = CaratulaService.actualizar_caratula(fecha_caratula, datos)
        return JsonResponse({
            "status": "success",
            "message": "Carátula actualizada exitosamente",
            "data": {
                "fecha": caratula.fecha_caratula.isoformat(),
                "consorcio": str(caratula.consorcio.cuit),
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
def eliminar_caratula(request, fecha_caratula):
    """Elimina una carátula."""
    try:
        CaratulaService.eliminar_caratula(fecha_caratula)
        return JsonResponse({
            "status": "success",
            "message": "Carátula eliminada exitosamente",
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e),
        }, status=404)
