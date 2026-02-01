"""Views para la app consorcios.

Fecha:
    31 - 01 - 2026
"""

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils.text import slugify
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from .services import ConsorcioService


@csrf_exempt
@require_http_methods(["POST"])
def crear_consorcio(request):
    """Crea un nuevo consorcio.
    
    POST: {
        "cuit": "string",
        "razon_social": "string",
        "calle": "string",
        "numero": int,
        "codigo_postal": "string",
        "ciudad": "string",
        "interes_por_mora": "decimal",
        "redondeo_aumento": "decimal"
    }
    """
    try:
        datos = json.loads(request.body)
        consorcio = ConsorcioService.crear_consorcio(datos)
        return JsonResponse({
            "status": "success",
            "message": "Consorcio creado exitosamente",
            "data": {
                "cuit": str(consorcio.cuit),
                "razon_social": consorcio.razon_social,
                "imagen_url": consorcio.imagen_url,
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
def obtener_consorcio(request, cuit):
    """Obtiene un consorcio específico."""
    try:
        consorcio = ConsorcioService.obtener_consorcio(cuit)
        return JsonResponse({
            "status": "success",
            "data": {
                "cuit": str(consorcio.cuit),
                "razon_social": consorcio.razon_social,
                "calle": consorcio.calle,
                "numero": consorcio.numero,
                "codigo_postal": consorcio.codigo_postal,
                "ciudad": consorcio.ciudad,
                "interes_por_mora": str(consorcio.interes_por_mora),
                "redondeo_aumento": str(consorcio.redondeo_aumento),
                "imagen_url": consorcio.imagen_url,
            }
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": f"Consorcio no encontrado: {str(e)}",
        }, status=404)


@csrf_exempt
@require_http_methods(["GET"])
def listar_consorcios(request):
    """Lista todos los consorcios."""
    try:
        consorcios = ConsorcioService.listar_consorcios()
        datos = [{
            "cuit": str(c.cuit),
            "razon_social": c.razon_social,
            "calle": c.calle,
            "numero": c.numero,
            "codigo_postal": c.codigo_postal,
            "ciudad": c.ciudad,
            "imagen_url": c.imagen_url,
        } for c in consorcios]
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
def actualizar_consorcio(request, cuit):
    """Actualiza un consorcio existente."""
    try:
        datos = json.loads(request.body)
        consorcio = ConsorcioService.actualizar_consorcio(cuit, datos)
        return JsonResponse({
            "status": "success",
            "message": "Consorcio actualizado exitosamente",
            "data": {
                "cuit": str(consorcio.cuit),
                "razon_social": consorcio.razon_social,
                "imagen_url": consorcio.imagen_url,
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
def eliminar_consorcio(request, cuit):
    """Elimina un consorcio."""
    try:
        ConsorcioService.eliminar_consorcio(cuit)
        return JsonResponse({
            "status": "success",
            "message": "Consorcio eliminado exitosamente",
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e),
        }, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def subir_imagen_consorcio(request, cuit):
    """Sube una imagen para el consorcio y guarda la URL en la BD."""
    try:
        consorcio = ConsorcioService.obtener_consorcio(cuit)
        if "image" not in request.FILES:
            return JsonResponse({
                "status": "error",
                "message": "No se encontró el archivo de imagen.",
            }, status=400)

        image_file = request.FILES["image"]
        base_name = slugify(consorcio.razon_social) or str(consorcio.cuit)
        ext = os.path.splitext(image_file.name)[1].lower() or ".jpg"
        file_name = f"{base_name}{ext}"

        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        storage = FileSystemStorage(location=settings.MEDIA_ROOT)
        if storage.exists(file_name):
            storage.delete(file_name)
        storage.save(file_name, image_file)

        consorcio.imagen_url = f"{settings.MEDIA_URL}{file_name}"
        consorcio.save(update_fields=["imagen_url"])

        return JsonResponse({
            "status": "success",
            "message": "Imagen subida exitosamente",
            "data": {
                "cuit": str(consorcio.cuit),
                "imagen_url": consorcio.imagen_url,
            }
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e),
        }, status=500)
