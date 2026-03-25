"""Views para la app proveedores.

Fecha:
    31 - 01 - 2026
"""

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

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
        return JsonResponse({
            "status": "success",
            "message": "Proveedor creado exitosamente",
            "data": {
                "cuit": str(proveedor.cuit),
                "razon_social": proveedor.razon_social,
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
def obtener_proveedor(request, cuit):
    """Obtiene un proveedor específico."""
    try:
        proveedor = ProveedorService.obtener_proveedor(cuit)
        return JsonResponse({
            "status": "success",
            "data": {
                "cuit": str(proveedor.cuit),
                "razon_social": proveedor.razon_social,
                "telefono": proveedor.telefono,
                "email": proveedor.email,
                "calle": proveedor.calle,
                "numero": proveedor.numero,
                "codigo_postal": proveedor.codigo_postal,
                "ciudad": proveedor.ciudad,
                "tipo_proveedor": proveedor.tipo_proveedor,
            }
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": f"Proveedor no encontrado: {str(e)}",
        }, status=404)


@csrf_exempt
@require_http_methods(["GET"])
def listar_proveedores(request):
    """Lista todos los proveedores."""
    try:
        proveedores = ProveedorService.listar_proveedores()
        datos = [{
            "cuit": str(p.cuit),
            "razon_social": p.razon_social,
            "ciudad": p.ciudad,
            "tipo_proveedor": p.tipo_proveedor,
        } for p in proveedores]
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
def listar_proveedores_por_tipo(request, tipo_proveedor):
    """Lista proveedores por tipo."""
    try:
        proveedores = ProveedorService.listar_proveedores_por_tipo(tipo_proveedor)
        datos = [{
            "cuit": str(p.cuit),
            "razon_social": p.razon_social,
            "ciudad": p.ciudad,
            "tipo_proveedor": p.tipo_proveedor,
        } for p in proveedores]
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
def actualizar_proveedor(request, cuit):
    """Actualiza un proveedor existente."""
    try:
        datos = json.loads(request.body)
        proveedor = ProveedorService.actualizar_proveedor(cuit, datos)
        return JsonResponse({
            "status": "success",
            "message": "Proveedor actualizado exitosamente",
            "data": {
                "cuit": str(proveedor.cuit),
                "razon_social": proveedor.razon_social,
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
def eliminar_proveedor(request, cuit):
    """Elimina un proveedor."""
    try:
        ProveedorService.eliminar_proveedor(cuit)
        return JsonResponse({
            "status": "success",
            "message": "Proveedor eliminado exitosamente",
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e),
        }, status=404)
