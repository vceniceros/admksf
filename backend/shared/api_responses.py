"""Helpers comunes para respuestas JSON de la API."""

from json import JSONDecodeError

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied, ValidationError
from django.http import JsonResponse


def success_response(data=None, message: str | None = None, status: int = 200, **extra):
    """Construye una respuesta exitosa consistente."""

    payload = {"status": "success"}
    if message:
        payload["message"] = message
    if data is not None:
        payload["data"] = data
    payload.update(extra)
    return JsonResponse(payload, status=status)


def error_response(message: str, status: int, errors: dict | None = None, **extra):
    """Construye una respuesta de error consistente."""

    payload = {
        "status": "error",
        "message": message,
    }
    if errors:
        payload["errors"] = errors
    payload.update(extra)
    return JsonResponse(payload, status=status)


def extract_validation_errors(exc: ValidationError) -> dict:
    """Normaliza errores de validacion de Django a un diccionario JSON serializable."""

    if hasattr(exc, "message_dict"):
        return exc.message_dict

    messages = getattr(exc, "messages", None)
    if messages:
        return {"non_field_errors": list(messages)}

    return {"non_field_errors": [str(exc)]}


def invalid_json_response():
    """Respuesta estándar para JSON inválido."""

    return error_response(
        "JSON inválido en el cuerpo de la solicitud.",
        400,
        errors={"body": ["No se pudo interpretar el JSON enviado."]},
    )


def validation_error_response(message: str, exc: ValidationError, status: int = 400):
    """Respuesta estándar para errores de validación."""

    return error_response(message, status, errors=extract_validation_errors(exc))


def exception_response(
    exc: Exception,
    *,
    validation_message: str = "Error de validación.",
    not_found_message: str = "Recurso no encontrado.",
    forbidden_message: str | None = None,
    unexpected_message: str | None = None,
):
    """Mapea excepciones frecuentes a respuestas HTTP fiables."""

    if isinstance(exc, JSONDecodeError):
        return invalid_json_response()

    if isinstance(exc, ValidationError):
        return validation_error_response(validation_message, exc)

    if isinstance(exc, PermissionDenied):
        return error_response(forbidden_message or str(exc) or "No autorizado.", 403)

    if isinstance(exc, ObjectDoesNotExist):
        return error_response(not_found_message, 404)

    return error_response(unexpected_message or str(exc) or "Ocurrió un error interno.", 500)