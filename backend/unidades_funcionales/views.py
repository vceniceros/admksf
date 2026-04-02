"""Views para la app unidades_funcionales.

Fecha:
    31 - 01 - 2026
"""

from django.core.exceptions import ValidationError
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from shared.api_responses import exception_response, success_response
from shared.auth import ensure_consorcio_access, filter_propietarios_queryset, filter_queryset_by_consorcios, get_request_user

from .services import UnidadFuncionalService


@csrf_exempt
@require_http_methods(["POST"])
def crear_unidad_funcional(request):
    """Crea una nueva unidad funcional.
    
    POST: {
        "numero_de_unidad_funcional": int,
        "consorcio": "string (cuit)",
        "tipo_de_unidad": "string",
        "estado_de_vivienda": "string",
        "superficie": "decimal",
        "propietario": "string (dni, optional)"
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
        unidad = UnidadFuncionalService.crear_unidad_funcional(datos)
        return success_response({
            "numero": unidad.numero_de_unidad_funcional,
            "tipo": unidad.tipo_de_unidad,
        }, message="Unidad funcional creada exitosamente", status=201)
    except Exception as e:
        return exception_response(e, validation_message="Error de validación al crear unidad funcional.")


@csrf_exempt
@require_http_methods(["GET"])
def obtener_unidad_funcional(request, numero):
    """Obtiene una unidad funcional específica."""
    try:
        usuario_autenticado = get_request_user(request)
        unidad = UnidadFuncionalService.obtener_unidad_funcional(numero)
        ensure_consorcio_access(usuario_autenticado, unidad.consorcio_id)
        return success_response({
            "numero": unidad.numero_de_unidad_funcional,
            "consorcio": str(unidad.consorcio.cuit),
            "tipo_de_unidad": unidad.tipo_de_unidad,
            "estado_de_vivienda": unidad.estado_de_vivienda,
            "superficie": str(unidad.superficie),
            "propietario": str(unidad.propietario.dni) if unidad.propietario else None,
        })
    except Exception as e:
        return exception_response(e, not_found_message="Unidad funcional no encontrada.")


@csrf_exempt
@require_http_methods(["GET"])
def listar_unidades_funcionales(request):
    """Lista todas las unidades funcionales."""
    try:
        usuario_autenticado = get_request_user(request)
        unidades = filter_queryset_by_consorcios(
            UnidadFuncionalService.listar_unidades_funcionales(),
            usuario_autenticado,
        )
        datos = [{
            "numero": u.numero_de_unidad_funcional,
            "consorcio": str(u.consorcio.cuit),
            "tipo": u.tipo_de_unidad,
            "estado": u.estado_de_vivienda,
            "superficie": str(u.superficie),
            "propietario": str(u.propietario.dni) if u.propietario else None,
        } for u in unidades]
        return success_response(datos, count=len(datos))
    except Exception as e:
        return exception_response(e)


@csrf_exempt
@require_http_methods(["GET"])
def listar_unidades_por_consorcio(request, cuit_consorcio):
    """Lista unidades funcionales de un consorcio."""
    try:
        usuario_autenticado = get_request_user(request)
        ensure_consorcio_access(usuario_autenticado, cuit_consorcio)
        unidades = UnidadFuncionalService.listar_unidades_por_consorcio(cuit_consorcio)
        datos = [{
            "numero": u.numero_de_unidad_funcional,
            "consorcio": str(u.consorcio.cuit),
            "tipo": u.tipo_de_unidad,
            "estado": u.estado_de_vivienda,
            "superficie": str(u.superficie),
            "propietario": str(u.propietario.dni) if u.propietario else None,
        } for u in unidades]
        return success_response(datos, count=len(datos))
    except Exception as e:
        return exception_response(e)


@csrf_exempt
@require_http_methods(["GET"])
def listar_unidades_por_propietario(request, dni_propietario):
    """Lista unidades funcionales de un propietario."""
    try:
        usuario_autenticado = get_request_user(request)
        unidades = filter_queryset_by_consorcios(
            UnidadFuncionalService.listar_unidades_por_propietario(dni_propietario),
            usuario_autenticado,
        )
        datos = [{
            "numero": u.numero_de_unidad_funcional,
            "consorcio": str(u.consorcio.cuit),
            "tipo": u.tipo_de_unidad,
            "estado": u.estado_de_vivienda,
            "superficie": str(u.superficie),
            "propietario": str(u.propietario.dni) if u.propietario else None,
        } for u in unidades]
        return success_response(datos, count=len(datos))
    except Exception as e:
        return exception_response(e)


@csrf_exempt
@require_http_methods(["PUT"])
def actualizar_unidad_funcional(request, numero):
    """Actualiza una unidad funcional existente."""
    try:
        usuario_autenticado = get_request_user(request)
        unidad_actual = UnidadFuncionalService.obtener_unidad_funcional(numero)
        ensure_consorcio_access(usuario_autenticado, unidad_actual.consorcio_id)

        datos = json.loads(request.body)
        if "consorcio" in datos:
            datos["consorcio_id"] = datos.pop("consorcio")
        if "propietario" in datos:
            datos["propietario_id"] = datos.pop("propietario")
        if datos.get("consorcio_id"):
            ensure_consorcio_access(usuario_autenticado, datos.get("consorcio_id"))
        unidad = UnidadFuncionalService.actualizar_unidad_funcional(numero, datos)
        return success_response({
            "numero": unidad.numero_de_unidad_funcional,
            "tipo": unidad.tipo_de_unidad,
        }, message="Unidad funcional actualizada exitosamente")
    except Exception as e:
        return exception_response(
            e,
            validation_message="Error de validación al actualizar unidad funcional.",
            not_found_message="Unidad funcional no encontrada.",
        )


@csrf_exempt
@require_http_methods(["DELETE"])
def eliminar_unidad_funcional(request, numero):
    """Elimina una unidad funcional."""
    try:
        usuario_autenticado = get_request_user(request)
        unidad = UnidadFuncionalService.obtener_unidad_funcional(numero)
        ensure_consorcio_access(usuario_autenticado, unidad.consorcio_id)
        UnidadFuncionalService.eliminar_unidad_funcional(numero)
        return success_response(message="Unidad funcional eliminada exitosamente")
    except Exception as e:
        return exception_response(e, not_found_message="Unidad funcional no encontrada.")
