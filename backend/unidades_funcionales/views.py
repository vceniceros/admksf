"""Views para la app unidades_funcionales.

Fecha:
    31 - 01 - 2026
"""

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

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
        datos = json.loads(request.body)
        if "consorcio" in datos:
            datos["consorcio_id"] = datos.pop("consorcio")
        if "propietario" in datos:
            datos["propietario_id"] = datos.pop("propietario")
        unidad = UnidadFuncionalService.crear_unidad_funcional(datos)
        return JsonResponse({
            "status": "success",
            "message": "Unidad funcional creada exitosamente",
            "data": {
                "numero": unidad.numero_de_unidad_funcional,
                "tipo": unidad.tipo_de_unidad,
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
def obtener_unidad_funcional(request, numero):
    """Obtiene una unidad funcional específica."""
    try:
        unidad = UnidadFuncionalService.obtener_unidad_funcional(numero)
        return JsonResponse({
            "status": "success",
            "data": {
                "numero": unidad.numero_de_unidad_funcional,
                "consorcio": str(unidad.consorcio.cuit),
                "tipo_de_unidad": unidad.tipo_de_unidad,
                "estado_de_vivienda": unidad.estado_de_vivienda,
                "superficie": str(unidad.superficie),
                "propietario": str(unidad.propietario.dni) if unidad.propietario else None,
            }
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": f"Unidad funcional no encontrada: {str(e)}",
        }, status=404)


@csrf_exempt
@require_http_methods(["GET"])
def listar_unidades_funcionales(request):
    """Lista todas las unidades funcionales."""
    try:
        unidades = UnidadFuncionalService.listar_unidades_funcionales()
        datos = [{
            "numero": u.numero_de_unidad_funcional,
            "consorcio": str(u.consorcio.cuit),
            "tipo": u.tipo_de_unidad,
            "estado": u.estado_de_vivienda,
            "superficie": str(u.superficie),
            "propietario": str(u.propietario.dni) if u.propietario else None,
        } for u in unidades]
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
def listar_unidades_por_consorcio(request, cuit_consorcio):
    """Lista unidades funcionales de un consorcio."""
    try:
        unidades = UnidadFuncionalService.listar_unidades_por_consorcio(cuit_consorcio)
        datos = [{
            "numero": u.numero_de_unidad_funcional,
            "consorcio": str(u.consorcio.cuit),
            "tipo": u.tipo_de_unidad,
            "estado": u.estado_de_vivienda,
            "superficie": str(u.superficie),
            "propietario": str(u.propietario.dni) if u.propietario else None,
        } for u in unidades]
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
def listar_unidades_por_propietario(request, dni_propietario):
    """Lista unidades funcionales de un propietario."""
    try:
        unidades = UnidadFuncionalService.listar_unidades_por_propietario(dni_propietario)
        datos = [{
            "numero": u.numero_de_unidad_funcional,
            "consorcio": str(u.consorcio.cuit),
            "tipo": u.tipo_de_unidad,
            "estado": u.estado_de_vivienda,
            "superficie": str(u.superficie),
            "propietario": str(u.propietario.dni) if u.propietario else None,
        } for u in unidades]
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
def actualizar_unidad_funcional(request, numero):
    """Actualiza una unidad funcional existente."""
    try:
        datos = json.loads(request.body)
        if "consorcio" in datos:
            datos["consorcio_id"] = datos.pop("consorcio")
        if "propietario" in datos:
            datos["propietario_id"] = datos.pop("propietario")
        unidad = UnidadFuncionalService.actualizar_unidad_funcional(numero, datos)
        return JsonResponse({
            "status": "success",
            "message": "Unidad funcional actualizada exitosamente",
            "data": {
                "numero": unidad.numero_de_unidad_funcional,
                "tipo": unidad.tipo_de_unidad,
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
def eliminar_unidad_funcional(request, numero):
    """Elimina una unidad funcional."""
    try:
        UnidadFuncionalService.eliminar_unidad_funcional(numero)
        return JsonResponse({
            "status": "success",
            "message": "Unidad funcional eliminada exitosamente",
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e),
        }, status=404)
