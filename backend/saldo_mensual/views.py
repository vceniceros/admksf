"""Views para la app saldo_mensual.

Fecha:
    31 - 01 - 2026
"""

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from .services import SaldoMensualService


@csrf_exempt
@require_http_methods(["POST"])
def crear_saldo_mensual(request):
    """Crea un nuevo saldo mensual.
    
    POST: {
        "numero_de_unidad_funcional": int,
        "consorcio": "string (cuit)",
        "mes_anio": "date",
        "saldo_inicial": "decimal",
        "total_gastos": "decimal",
        "total_pagos": "decimal",
        "saldo_final": "decimal",
        "fecha_cierre": "datetime (optional)"
    }
    """
    try:
        datos = json.loads(request.body)
        if "consorcio" in datos:
            datos["consorcio_id"] = datos.pop("consorcio")
        saldo = SaldoMensualService.crear_saldo_mensual(datos)
        return JsonResponse({
            "status": "success",
            "message": "Saldo mensual creado exitosamente",
            "data": {
                "id": saldo.id_saldo_mensual,
                "saldo_final": str(saldo.saldo_final),
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
def obtener_saldo_mensual(request, id_saldo):
    """Obtiene un saldo mensual específico."""
    try:
        saldo = SaldoMensualService.obtener_saldo_mensual(id_saldo)
        return JsonResponse({
            "status": "success",
            "data": {
                "id": saldo.id_saldo_mensual,
                "numero_unidad": saldo.numero_de_unidad_funcional,
                "consorcio": str(saldo.consorcio.cuit),
                "mes_anio": str(saldo.mes_anio),
                "saldo_inicial": str(saldo.saldo_inicial),
                "total_gastos": str(saldo.total_gastos),
                "total_pagos": str(saldo.total_pagos),
                "saldo_final": str(saldo.saldo_final),
                "fecha_cierre": saldo.fecha_cierre.isoformat() if saldo.fecha_cierre else None,
            }
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": f"Saldo mensual no encontrado: {str(e)}",
        }, status=404)


@csrf_exempt
@require_http_methods(["GET"])
def listar_saldos_mensuales(request):
    """Lista todos los saldos mensuales."""
    try:
        saldos = SaldoMensualService.listar_saldos_mensuales()
        datos = [{
            "id": s.id_saldo_mensual,
            "numero_unidad": s.numero_de_unidad_funcional,
            "mes_anio": str(s.mes_anio),
            "saldo_final": str(s.saldo_final),
        } for s in saldos]
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
def listar_saldos_por_consorcio(request, cuit_consorcio):
    """Lista saldos mensuales de un consorcio."""
    try:
        saldos = SaldoMensualService.listar_saldos_por_consorcio(cuit_consorcio)
        datos = [{
            "id": s.id_saldo_mensual,
            "numero_unidad": s.numero_de_unidad_funcional,
            "mes_anio": str(s.mes_anio),
            "saldo_final": str(s.saldo_final),
        } for s in saldos]
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
def listar_saldos_por_unidad_funcional(request, numero_unidad):
    """Lista saldos mensuales de una unidad funcional."""
    try:
        saldos = SaldoMensualService.listar_saldos_por_unidad_funcional(numero_unidad)
        datos = [{
            "id": s.id_saldo_mensual,
            "mes_anio": str(s.mes_anio),
            "saldo_final": str(s.saldo_final),
        } for s in saldos]
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
def actualizar_saldo_mensual(request, id_saldo):
    """Actualiza un saldo mensual existente."""
    try:
        datos = json.loads(request.body)
        if "consorcio" in datos:
            datos["consorcio_id"] = datos.pop("consorcio")
        saldo = SaldoMensualService.actualizar_saldo_mensual(id_saldo, datos)
        return JsonResponse({
            "status": "success",
            "message": "Saldo mensual actualizado exitosamente",
            "data": {
                "id": saldo.id_saldo_mensual,
                "saldo_final": str(saldo.saldo_final),
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
def eliminar_saldo_mensual(request, id_saldo):
    """Elimina un saldo mensual."""
    try:
        SaldoMensualService.eliminar_saldo_mensual(id_saldo)
        return JsonResponse({
            "status": "success",
            "message": "Saldo mensual eliminado exitosamente",
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e),
        }, status=404)
