"""Views para la app pagos.

Fecha:
    31 - 01 - 2026
"""

from django.core.exceptions import ValidationError
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from shared.api_responses import exception_response, success_response
from shared.auth import ensure_consorcio_access, filter_queryset_by_consorcios, get_request_user

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
        usuario_autenticado = get_request_user(request)
        datos = json.loads(request.body)
        if "consorcio" in datos:
            datos["consorcio_id"] = datos.pop("consorcio")
        if "propietario" in datos:
            datos["propietario_id"] = datos.pop("propietario")
        ensure_consorcio_access(usuario_autenticado, datos.get("consorcio_id"))
        pago = PagoService.crear_pago(datos)
        return success_response({
            "id": pago.id_pago,
            "monto": str(pago.monto),
        }, message="Pago creado exitosamente", status=201)
    except Exception as e:
        return exception_response(e, validation_message="Error de validación al crear pago.")


@csrf_exempt
@require_http_methods(["GET"])
def obtener_pago(request, id_pago):
    """Obtiene un pago específico."""
    try:
        usuario_autenticado = get_request_user(request)
        pago = PagoService.obtener_pago(id_pago)
        ensure_consorcio_access(usuario_autenticado, pago.consorcio_id)
        return success_response({
            "id": pago.id_pago,
            "numero_unidad": pago.numero_de_unidad_funcional,
            "consorcio": str(pago.consorcio.cuit),
            "propietario": str(pago.propietario.dni),
            "monto": str(pago.monto),
            "estado_pago": pago.estado_pago,
            "fecha_pago": pago.fecha_pago.isoformat(),
        })
    except Exception as e:
        return exception_response(e, not_found_message="Pago no encontrado.")


@csrf_exempt
@require_http_methods(["GET"])
def listar_pagos(request):
    """Lista todos los pagos."""
    try:
        usuario_autenticado = get_request_user(request)
        pagos = filter_queryset_by_consorcios(PagoService.listar_pagos(), usuario_autenticado)
        datos = [{
            "id": p.id_pago,
            "numero_unidad": p.numero_de_unidad_funcional,
            "consorcio": str(p.consorcio.cuit),
            "propietario": str(p.propietario.dni),
            "monto": str(p.monto),
            "estado_pago": p.estado_pago,
            "fecha_pago": p.fecha_pago.isoformat(),
        } for p in pagos]
        return success_response(datos, count=len(datos))
    except Exception as e:
        return exception_response(e)


@csrf_exempt
@require_http_methods(["GET"])
def listar_pagos_por_consorcio(request, cuit_consorcio):
    """Lista pagos de un consorcio."""
    try:
        usuario_autenticado = get_request_user(request)
        ensure_consorcio_access(usuario_autenticado, cuit_consorcio)
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
        return success_response(datos, count=len(datos))
    except Exception as e:
        return exception_response(e)


@csrf_exempt
@require_http_methods(["GET"])
def listar_pagos_por_propietario(request, dni_propietario):
    """Lista pagos de un propietario."""
    try:
        usuario_autenticado = get_request_user(request)
        pagos = filter_queryset_by_consorcios(
            PagoService.listar_pagos_por_propietario(dni_propietario),
            usuario_autenticado,
        )
        datos = [{
            "id": p.id_pago,
            "numero_unidad": p.numero_de_unidad_funcional,
            "consorcio": str(p.consorcio.cuit),
            "propietario": str(p.propietario.dni),
            "monto": str(p.monto),
            "estado_pago": p.estado_pago,
            "fecha_pago": p.fecha_pago.isoformat(),
        } for p in pagos]
        return success_response(datos, count=len(datos))
    except Exception as e:
        return exception_response(e)


@csrf_exempt
@require_http_methods(["GET"])
def listar_pagos_por_unidad_funcional(request, numero_unidad):
    """Lista pagos de una unidad funcional."""
    try:
        usuario_autenticado = get_request_user(request)
        pagos = filter_queryset_by_consorcios(
            PagoService.listar_pagos_por_unidad_funcional(numero_unidad),
            usuario_autenticado,
        )
        datos = [{
            "id": p.id_pago,
            "numero_unidad": p.numero_de_unidad_funcional,
            "consorcio": str(p.consorcio.cuit),
            "propietario": str(p.propietario.dni),
            "monto": str(p.monto),
            "estado_pago": p.estado_pago,
            "fecha_pago": p.fecha_pago.isoformat(),
        } for p in pagos]
        return success_response(datos, count=len(datos))
    except Exception as e:
        return exception_response(e)


@csrf_exempt
@require_http_methods(["PUT"])
def actualizar_pago(request, id_pago):
    """Actualiza un pago existente."""
    try:
        usuario_autenticado = get_request_user(request)
        pago_actual = PagoService.obtener_pago(id_pago)
        ensure_consorcio_access(usuario_autenticado, pago_actual.consorcio_id)

        datos = json.loads(request.body)
        if "consorcio" in datos:
            datos["consorcio_id"] = datos.pop("consorcio")
        if "propietario" in datos:
            datos["propietario_id"] = datos.pop("propietario")
        if datos.get("consorcio_id"):
            ensure_consorcio_access(usuario_autenticado, datos.get("consorcio_id"))
        pago = PagoService.actualizar_pago(id_pago, datos)
        return success_response({
            "id": pago.id_pago,
            "monto": str(pago.monto),
        }, message="Pago actualizado exitosamente")
    except Exception as e:
        return exception_response(
            e,
            validation_message="Error de validación al actualizar pago.",
            not_found_message="Pago no encontrado.",
        )


@csrf_exempt
@require_http_methods(["DELETE"])
def eliminar_pago(request, id_pago):
    """Elimina un pago."""
    try:
        usuario_autenticado = get_request_user(request)
        pago = PagoService.obtener_pago(id_pago)
        ensure_consorcio_access(usuario_autenticado, pago.consorcio_id)
        PagoService.eliminar_pago(id_pago)
        return success_response(message="Pago eliminado exitosamente")
    except Exception as e:
        return exception_response(e, not_found_message="Pago no encontrado.")