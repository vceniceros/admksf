"""Views para la app consorcios.

Fecha:
    31 - 01 - 2026
"""

from django.http import JsonResponse
from django.utils.text import slugify
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from json import JSONDecodeError

from shared.api_responses import exception_response, success_response
from shared.auth import ensure_consorcio_access, get_accessible_consorcios, get_request_user, is_superusuario

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
        usuario_autenticado = get_request_user(request)
        datos = json.loads(request.body)

        if "usuario" in datos:
            datos["usuario_id"] = datos.pop("usuario")

        if not is_superusuario(usuario_autenticado):
            datos["usuario_id"] = usuario_autenticado.id

        consorcio = ConsorcioService.crear_consorcio(datos)
        return success_response({
            "cuit": str(consorcio.cuit),
            "razon_social": consorcio.razon_social,
            "imagen_url": consorcio.imagen_url,
        }, message="Consorcio creado exitosamente", status=201)
    except Exception as e:
        return exception_response(e, validation_message="Error de validación al crear consorcio.")


@csrf_exempt
@require_http_methods(["GET"])
def obtener_consorcio(request, cuit):
    """Obtiene un consorcio específico."""
    try:
        usuario_autenticado = get_request_user(request)
        consorcio = ensure_consorcio_access(usuario_autenticado, cuit)
        return success_response({
            "cuit": str(consorcio.cuit),
            "razon_social": consorcio.razon_social,
            "calle": consorcio.calle,
            "numero": consorcio.numero,
            "codigo_postal": consorcio.codigo_postal,
            "ciudad": consorcio.ciudad,
            "interes_por_mora": str(consorcio.interes_por_mora),
            "redondeo_aumento": str(consorcio.redondeo_aumento),
            "imagen_url": consorcio.imagen_url,
        })
    except Exception as e:
        return exception_response(e, not_found_message="Consorcio no encontrado.")


@csrf_exempt
@require_http_methods(["GET"])
def listar_consorcios(request):
    """Lista todos los consorcios."""
    try:
        usuario_autenticado = get_request_user(request)
        consorcios = get_accessible_consorcios(usuario_autenticado)
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
        return exception_response(e)


@csrf_exempt
@require_http_methods(["PUT"])
def actualizar_consorcio(request, cuit):
    """Actualiza un consorcio existente."""
    try:
        usuario_autenticado = get_request_user(request)
        ensure_consorcio_access(usuario_autenticado, cuit)
        datos = json.loads(request.body)

        if "usuario" in datos:
            datos["usuario_id"] = datos.pop("usuario")

        if not is_superusuario(usuario_autenticado):
            datos.pop("usuario", None)
            datos["usuario_id"] = usuario_autenticado.id

        consorcio = ConsorcioService.actualizar_consorcio(cuit, datos)
        return success_response({
            "cuit": str(consorcio.cuit),
            "razon_social": consorcio.razon_social,
            "imagen_url": consorcio.imagen_url,
        }, message="Consorcio actualizado exitosamente")
    except Exception as e:
        return exception_response(
            e,
            validation_message="Error de validación al actualizar consorcio.",
            not_found_message="Consorcio no encontrado.",
        )


@csrf_exempt
@require_http_methods(["DELETE"])
def eliminar_consorcio(request, cuit):
    """Elimina un consorcio."""
    try:
        usuario_autenticado = get_request_user(request)
        ensure_consorcio_access(usuario_autenticado, cuit)
        ConsorcioService.eliminar_consorcio(cuit)
        return success_response(message="Consorcio eliminado exitosamente")
    except Exception as e:
        return exception_response(e, not_found_message="Consorcio no encontrado.")


@csrf_exempt
@require_http_methods(["POST"])
def subir_imagen_consorcio(request, cuit):
    """Sube una imagen para el consorcio y guarda la URL en la BD."""
    try:
        usuario_autenticado = get_request_user(request)
        consorcio = ensure_consorcio_access(usuario_autenticado, cuit)
        if "image" not in request.FILES:
            return exception_response(ValidationError({"image": ["No se encontró el archivo de imagen."]}), validation_message="No se pudo subir la imagen del consorcio.")

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

        return success_response({
            "cuit": str(consorcio.cuit),
            "imagen_url": consorcio.imagen_url,
        }, message="Imagen subida exitosamente")
    except Exception as e:
        return exception_response(e, validation_message="No se pudo subir la imagen del consorcio.")
