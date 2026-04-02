"""Views para la app saldo_mensual.

Fecha:
    31 - 01 - 2026
"""

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from shared.api_responses import exception_response, success_response
from shared.auth import ensure_consorcio_access, filter_queryset_by_consorcios, get_request_user

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
        usuario_autenticado = get_request_user(request)
        datos = json.loads(request.body)
        if "consorcio" in datos:
            datos["consorcio_id"] = datos.pop("consorcio")
        ensure_consorcio_access(usuario_autenticado, datos.get("consorcio_id"))
        saldo = SaldoMensualService.crear_saldo_mensual(datos)
        return success_response({
            "id": saldo.id_saldo_mensual,
            "saldo_final": str(saldo.saldo_final),
        }, message="Saldo mensual creado exitosamente", status=201)
    except Exception as e:
        return exception_response(e, validation_message="Error de validación al crear saldo mensual.")


@csrf_exempt
@require_http_methods(["GET"])
def obtener_saldo_mensual(request, id_saldo):
    """Obtiene un saldo mensual específico."""
    try:
        usuario_autenticado = get_request_user(request)
        saldo = SaldoMensualService.obtener_saldo_mensual(id_saldo)
        ensure_consorcio_access(usuario_autenticado, saldo.consorcio_id)
        return success_response({
            "id": saldo.id_saldo_mensual,
            "numero_unidad": saldo.numero_de_unidad_funcional,
            "consorcio": str(saldo.consorcio.cuit),
            "mes_anio": str(saldo.mes_anio),
            "saldo_inicial": str(saldo.saldo_inicial),
            "total_gastos": str(saldo.total_gastos),
            "total_pagos": str(saldo.total_pagos),
            "saldo_final": str(saldo.saldo_final),
            "fecha_cierre": saldo.fecha_cierre.isoformat() if saldo.fecha_cierre else None,
        })
    except Exception as e:
        return exception_response(e, not_found_message="Saldo mensual no encontrado.")


@csrf_exempt
@require_http_methods(["GET"])
def listar_saldos_mensuales(request):
    """Lista todos los saldos mensuales."""
    try:
        usuario_autenticado = get_request_user(request)
        saldos = filter_queryset_by_consorcios(
            SaldoMensualService.listar_saldos_mensuales(),
            usuario_autenticado,
        )
        datos = [{
            "id": s.id_saldo_mensual,
            "numero_unidad": s.numero_de_unidad_funcional,
            "mes_anio": str(s.mes_anio),
            "saldo_final": str(s.saldo_final),
        } for s in saldos]
        return success_response(datos, count=len(datos))
    except Exception as e:
        return exception_response(e)


@csrf_exempt
@require_http_methods(["GET"])
def listar_saldos_por_consorcio(request, cuit_consorcio):
    """Lista saldos mensuales de un consorcio."""
    try:
        usuario_autenticado = get_request_user(request)
        ensure_consorcio_access(usuario_autenticado, cuit_consorcio)
        saldos = SaldoMensualService.listar_saldos_por_consorcio(cuit_consorcio)
        datos = [{
            "id": s.id_saldo_mensual,
            "numero_unidad": s.numero_de_unidad_funcional,
            "mes_anio": str(s.mes_anio),
            "saldo_final": str(s.saldo_final),
        } for s in saldos]
        return success_response(datos, count=len(datos))
    except Exception as e:
        return exception_response(e)


@csrf_exempt
@require_http_methods(["GET"])
def listar_saldos_por_unidad_funcional(request, numero_unidad):
    """Lista saldos mensuales de una unidad funcional."""
    try:
        usuario_autenticado = get_request_user(request)
        saldos = filter_queryset_by_consorcios(
            SaldoMensualService.listar_saldos_por_unidad_funcional(numero_unidad),
            usuario_autenticado,
        )
        datos = [{
            "id": s.id_saldo_mensual,
            "mes_anio": str(s.mes_anio),
            "saldo_final": str(s.saldo_final),
        } for s in saldos]
        return success_response(datos, count=len(datos))
    except Exception as e:
        return exception_response(e)


@csrf_exempt
@require_http_methods(["PUT"])
def actualizar_saldo_mensual(request, id_saldo):
    """Actualiza un saldo mensual existente."""
    try:
        usuario_autenticado = get_request_user(request)
        datos = json.loads(request.body)
        saldo_actual = SaldoMensualService.obtener_saldo_mensual(id_saldo)
        ensure_consorcio_access(usuario_autenticado, saldo_actual.consorcio_id)
        if "consorcio" in datos:
            datos["consorcio_id"] = datos.pop("consorcio")
        if "consorcio_id" in datos:
            ensure_consorcio_access(usuario_autenticado, datos.get("consorcio_id"))
        saldo = SaldoMensualService.actualizar_saldo_mensual(id_saldo, datos)
        return success_response({
            "id": saldo.id_saldo_mensual,
            "saldo_final": str(saldo.saldo_final),
        }, message="Saldo mensual actualizado exitosamente")
    except Exception as e:
        return exception_response(
            e,
            validation_message="Error de validación al actualizar saldo mensual.",
            not_found_message="Saldo mensual no encontrado.",
        )


@csrf_exempt
@require_http_methods(["DELETE"])
def eliminar_saldo_mensual(request, id_saldo):
    """Elimina un saldo mensual."""
    try:
        usuario_autenticado = get_request_user(request)
        saldo = SaldoMensualService.obtener_saldo_mensual(id_saldo)
        ensure_consorcio_access(usuario_autenticado, saldo.consorcio_id)
        SaldoMensualService.eliminar_saldo_mensual(id_saldo)
        return success_response(message="Saldo mensual eliminado exitosamente")
    except Exception as e:
        return exception_response(e, not_found_message="Saldo mensual no encontrado.")
