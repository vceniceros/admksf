"""Views para la app expensas.

Fecha:
    14 - 02 - 2026
"""

import json

from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from shared.api_responses import exception_response, success_response
from shared.auth import ensure_consorcio_access, filter_queryset_by_consorcios, get_request_user

from .services import LiquidacionService
from .models import ExpensaTemplate


@csrf_exempt
@require_http_methods(["POST"])
def liquidar_expensa(request):
    """Genera una liquidación en base a un template.

    POST: {
        "template_id": 1,
        "consorcio": "20304050607",
        "periodo": "2026-02",
        "cerrar": true,
        "parametros": {
            "conceptos_particulares": [
                {"unidad": 1, "column_id": "reparaciones", "monto": "1200.00"}
            ],
            "coeficientes_custom": {"1": "0.6", "2": "0.4"}
        }
    }
    """

    try:
        usuario_autenticado = get_request_user(request)
        payload = json.loads(request.body)
        consorcio_id = payload.get("consorcio")
        ensure_consorcio_access(usuario_autenticado, consorcio_id)

        template_id = payload.get("template_id")
        if template_id:
            template = ExpensaTemplate.objects.get(pk=template_id)
            if template.consorcio_id:
                ensure_consorcio_access(usuario_autenticado, template.consorcio_id)
                if consorcio_id and template.consorcio_id != consorcio_id:
                    raise ValidationError("El template no pertenece al consorcio indicado.")

        resultado = LiquidacionService.liquidar(payload)
        return success_response(resultado)
    except Exception as exc:
        return exception_response(exc, validation_message="Error de validación al liquidar expensas.")


@csrf_exempt
@require_http_methods(["GET"])
def listar_templates(request):
    """Lista templates de expensa.

    GET: /api/expensas/templates/?consorcio=<cuit>
    """

    try:
        usuario_autenticado = get_request_user(request)
        consorcio = request.GET.get("consorcio")
        queryset = filter_queryset_by_consorcios(ExpensaTemplate.objects.all(), usuario_autenticado)
        if consorcio:
            ensure_consorcio_access(usuario_autenticado, consorcio)
            queryset = queryset.filter(consorcio_id=consorcio)
        templates = [
            {
                "id": template.id_expensa_template,
                "consorcio": template.consorcio_id,
                "nombre": template.nombre,
                "version": template.version,
                "activo": template.activo,
            }
            for template in queryset.order_by("-creado_en")
        ]
        return success_response(templates)
    except Exception as exc:
        return exception_response(exc)


@csrf_exempt
@require_http_methods(["GET"])
def listar_templates_por_consorcio(request, cuit_consorcio):
    """Lista templates de expensa por consorcio."""
    try:
        usuario_autenticado = get_request_user(request)
        ensure_consorcio_access(usuario_autenticado, cuit_consorcio)
        queryset = ExpensaTemplate.objects.filter(consorcio_id=cuit_consorcio)
        templates = [
            {
                "id": template.id_expensa_template,
                "consorcio": template.consorcio_id,
                "nombre": template.nombre,
                "version": template.version,
                "activo": template.activo,
            }
            for template in queryset.order_by("-creado_en")
        ]
        return success_response(templates)
    except Exception as exc:
        return exception_response(exc)


@csrf_exempt
@require_http_methods(["POST"])
def crear_template(request):
    """Crea un template de expensa."""

    try:
        usuario_autenticado = get_request_user(request)
        payload = json.loads(request.body)
        ensure_consorcio_access(usuario_autenticado, payload.get("consorcio"))
        template = ExpensaTemplate.objects.create(
            consorcio_id=payload.get("consorcio"),
            nombre=payload.get("nombre"),
            version=payload.get("version", 1),
            config=payload.get("config", {}),
            activo=payload.get("activo", True),
        )
        return success_response(
            {
                "id": template.id_expensa_template,
                "consorcio": template.consorcio_id,
                "nombre": template.nombre,
                "version": template.version,
                "activo": template.activo,
            },
            status=201,
        )
    except Exception as exc:
        return exception_response(exc, validation_message="Error de validación al crear template de expensa.")


@csrf_exempt
@require_http_methods(["GET"])
def obtener_template(request, template_id):
    """Obtiene un template de expensa por ID."""

    try:
        usuario_autenticado = get_request_user(request)
        template = ExpensaTemplate.objects.get(pk=template_id)
        if template.consorcio_id:
            ensure_consorcio_access(usuario_autenticado, template.consorcio_id)
        return success_response(
            {
                "id": template.id_expensa_template,
                "consorcio": template.consorcio_id,
                "nombre": template.nombre,
                "version": template.version,
                "activo": template.activo,
                "config": template.config,
            }
        )
    except Exception as exc:
        return exception_response(exc, not_found_message="Template no encontrado.")


@csrf_exempt
@require_http_methods(["PUT"])
def actualizar_template(request, template_id):
    """Actualiza un template de expensa."""

    try:
        usuario_autenticado = get_request_user(request)
        payload = json.loads(request.body)
        template = ExpensaTemplate.objects.get(pk=template_id)
        if template.consorcio_id:
            ensure_consorcio_access(usuario_autenticado, template.consorcio_id)
        if "consorcio" in payload:
            ensure_consorcio_access(usuario_autenticado, payload.get("consorcio"))
        for field in ["consorcio", "nombre", "version", "config", "activo"]:
            if field in payload:
                if field == "consorcio":
                    template.consorcio_id = payload[field]
                else:
                    setattr(template, field, payload[field])
        template.save()
        return success_response(
            {
                "id": template.id_expensa_template,
                "consorcio": template.consorcio_id,
                "nombre": template.nombre,
                "version": template.version,
                "activo": template.activo,
                "config": template.config,
            }
        )
    except Exception as exc:
        return exception_response(
            exc,
            validation_message="Error de validación al actualizar template de expensa.",
            not_found_message="Template no encontrado.",
        )


@csrf_exempt
@require_http_methods(["DELETE"])
def eliminar_template(request, template_id):
    """Elimina un template de expensa."""

    try:
        usuario_autenticado = get_request_user(request)
        template = ExpensaTemplate.objects.get(pk=template_id)
        if template.consorcio_id:
            ensure_consorcio_access(usuario_autenticado, template.consorcio_id)
        template.delete()
        return success_response(message="Template eliminado.")
    except Exception as exc:
        return exception_response(exc, not_found_message="Template no encontrado.")
