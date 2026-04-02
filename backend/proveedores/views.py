"""Views para la app proveedores.

Fecha:
    31 - 01 - 2026
"""

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from shared.api_responses import exception_response, success_response
from shared.auth import ensure_proveedor_access, filter_proveedores_queryset, get_request_user

from .services import ProveedorService


@csrf_exempt
@require_http_methods(["POST"])
def crear_proveedor(request):
    """Crea un nuevo proveedor.
    
    POST: {
        "cuit": "string",
        "razon_social": "string",
        "telefono": "string (optional)",
        "email": "string (optional)",
        "calle": "string",
        "numero": int,
        "codigo_postal": "string",
        "ciudad": "string",
        "tipo_proveedor": "string"
    }
    """
    try:
        datos = json.loads(request.body)
        proveedor = ProveedorService.crear_proveedor(datos)
        return success_response({
            "cuit": str(proveedor.cuit),
            "razon_social": proveedor.razon_social,
        }, message="Proveedor creado exitosamente", status=201)
    except Exception as e:
        return exception_response(e, validation_message="Error de validación al crear proveedor.")


@csrf_exempt
@require_http_methods(["GET"])
def obtener_proveedor(request, cuit):
    """Obtiene un proveedor específico."""
    try:
        usuario_autenticado = get_request_user(request)
        proveedor = ensure_proveedor_access(
            ProveedorService.listar_proveedores(),
            usuario_autenticado,
            cuit,
        )
        return success_response({
            "cuit": str(proveedor.cuit),
            "razon_social": proveedor.razon_social,
            "telefono": proveedor.telefono,
            "email": proveedor.email,
            "calle": proveedor.calle,
            "numero": proveedor.numero,
            "codigo_postal": proveedor.codigo_postal,
            "ciudad": proveedor.ciudad,
            "tipo_proveedor": proveedor.tipo_proveedor,
        })
    except Exception as e:
        return exception_response(e, not_found_message="Proveedor no encontrado.")


@csrf_exempt
@require_http_methods(["GET"])
def listar_proveedores(request):
    """Lista todos los proveedores."""
    try:
        usuario_autenticado = get_request_user(request)
        proveedores = filter_proveedores_queryset(
            ProveedorService.listar_proveedores(),
            usuario_autenticado,
        )
        datos = [{
            "cuit": str(p.cuit),
            "razon_social": p.razon_social,
            "ciudad": p.ciudad,
            "tipo_proveedor": p.tipo_proveedor,
        } for p in proveedores]
        return success_response(datos, count=len(datos))
    except Exception as e:
        return exception_response(e)


@csrf_exempt
@require_http_methods(["GET"])
def listar_proveedores_por_tipo(request, tipo_proveedor):
    """Lista proveedores por tipo."""
    try:
        usuario_autenticado = get_request_user(request)
        proveedores = filter_proveedores_queryset(
            ProveedorService.listar_proveedores_por_tipo(tipo_proveedor),
            usuario_autenticado,
        )
        datos = [{
            "cuit": str(p.cuit),
            "razon_social": p.razon_social,
            "ciudad": p.ciudad,
            "tipo_proveedor": p.tipo_proveedor,
        } for p in proveedores]
        return success_response(datos, count=len(datos))
    except Exception as e:
        return exception_response(e)


@csrf_exempt
@require_http_methods(["PUT"])
def actualizar_proveedor(request, cuit):
    """Actualiza un proveedor existente."""
    try:
        usuario_autenticado = get_request_user(request)
        ensure_proveedor_access(
            ProveedorService.listar_proveedores(),
            usuario_autenticado,
            cuit,
        )
        datos = json.loads(request.body)
        proveedor = ProveedorService.actualizar_proveedor(cuit, datos)
        return success_response({
            "cuit": str(proveedor.cuit),
            "razon_social": proveedor.razon_social,
        }, message="Proveedor actualizado exitosamente")
    except Exception as e:
        return exception_response(
            e,
            validation_message="Error de validación al actualizar proveedor.",
            not_found_message="Proveedor no encontrado.",
        )


@csrf_exempt
@require_http_methods(["DELETE"])
def eliminar_proveedor(request, cuit):
    """Elimina un proveedor."""
    try:
        usuario_autenticado = get_request_user(request)
        ensure_proveedor_access(
            ProveedorService.listar_proveedores(),
            usuario_autenticado,
            cuit,
        )
        ProveedorService.eliminar_proveedor(cuit)
        return success_response(message="Proveedor eliminado exitosamente")
    except Exception as e:
        return exception_response(e, not_found_message="Proveedor no encontrado.")
