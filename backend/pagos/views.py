"""Views para la app pagos.

Fecha:
    31 - 01 - 2026
"""

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from .services import PagoService


@csrf_exempt
@require_http_methods(["POST"])
def crear_pago(request):
    """Crea un nuevo pago.
    
    POST: {
        "numero_de_unidad_funcional": int,
        "consorcio": "string (cuit)",
        "propietario": "string (dni)",
        "monto": "decimal",
        "estado_pago": "string (optional)",
        "fecha_pago": "datetime (optional)"
    }
    """
    try:
        datos = json.loads(request.body)
        if "consorcio" in datos:
            datos["consorcio_id"] = datos.pop("consorcio")
        if "propietario" in datos:
            datos["propietario_id"] = datos.pop("propietario")
        pago = PagoService.crear_pago(datos)
        return JsonResponse({
            "status": "success",
            "message": "Pago creado exitosamente",
            "data": {
                "id": pago.id_pago,
                "monto": str(pago.monto),
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
def obtener_pago(request, id_pago):
    """Obtiene un pago específico."""
    try:
        pago = PagoService.obtener_pago(id_pago)
        return JsonResponse({
            "status": "success",
            "data": {
                "id": pago.id_pago,
                "numero_unidad": pago.numero_de_unidad_funcional,
                "consorcio": str(pago.consorcio.cuit),
                "propietario": str(pago.propietario.dni),
                "monto": str(pago.monto),
                "estado_pago": pago.estado_pago,
                "fecha_pago": pago.fecha_pago.isoformat(),
            }
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": f"Pago no encontrado: {str(e)}",
        }, status=404)


@csrf_exempt
@require_http_methods(["GET"])
def listar_pagos(request):
    """Lista todos los pagos."""
    try:
        pagos = PagoService.listar_pagos()
        datos = [{
            "id": p.id_pago,
            "numero_unidad": p.numero_de_unidad_funcional,
            "consorcio": str(p.consorcio.cuit),
            "propietario": str(p.propietario.dni),
            "monto": str(p.monto),
            "estado_pago": p.estado_pago,
            "fecha_pago": p.fecha_pago.isoformat(),
        } for p in pagos]
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
def listar_pagos_por_consorcio(request, cuit_consorcio):
    """Lista pagos de un consorcio."""
    try:
        pagos = PagoService.listar_pagos_por_consorcio(cuit_consorcio)
        datos = [{
            "id": p.id_pago,
            "numero_unidad": p.numero_de_unidad_funcional,
            "consorcio": str(p.consorcio.cuit),
            "propietario": str(p.propietario.dni),
            "monto": str(p.monto),
            "estado_pago": p.estado_pago,
            "fecha_pago": p.fecha_pago.isoformat(),
        } for p in pagos]
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
def listar_pagos_por_propietario(request, dni_propietario):
    """Lista pagos de un propietario."""
    try:
        pagos = PagoService.listar_pagos_por_propietario(dni_propietario)
        datos = [{
            "id": p.id_pago,
            "numero_unidad": p.numero_de_unidad_funcional,
            "consorcio": str(p.consorcio.cuit),
            "propietario": str(p.propietario.dni),
            "monto": str(p.monto),
            "estado_pago": p.estado_pago,
            "fecha_pago": p.fecha_pago.isoformat(),
        } for p in pagos]
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
def listar_pagos_por_unidad_funcional(request, numero_unidad):
    """Lista pagos de una unidad funcional."""
    try:
        pagos = PagoService.listar_pagos_por_unidad_funcional(numero_unidad)
        datos = [{
            "id": p.id_pago,
            "numero_unidad": p.numero_de_unidad_funcional,
            "consorcio": str(p.consorcio.cuit),
            "propietario": str(p.propietario.dni),
            "monto": str(p.monto),
            "estado_pago": p.estado_pago,
            "fecha_pago": p.fecha_pago.isoformat(),
        } for p in pagos]
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
def actualizar_pago(request, id_pago):
    """Actualiza un pago existente."""
    try:
        datos = json.loads(request.body)
        if "consorcio" in datos:
            datos["consorcio_id"] = datos.pop("consorcio")
        if "propietario" in datos:
            datos["propietario_id"] = datos.pop("propietario")
        pago = PagoService.actualizar_pago(id_pago, datos)
        return JsonResponse({
            "status": "success",
            "message": "Pago actualizado exitosamente",
            "data": {
                "id": pago.id_pago,
                "monto": str(pago.monto),
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
def eliminar_pago(request, id_pago):
    """Elimina un pago."""
    try:
        PagoService.eliminar_pago(id_pago)
        return JsonResponse({
            "status": "success",
            "message": "Pago eliminado exitosamente",
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e),
        }, status=404)