"""Views para la app expensas.

Fecha:
    14 - 02 - 2026
"""

import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

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
        payload = json.loads(request.body)
        resultado = LiquidacionService.liquidar(payload)
        status_code = 201 if payload.get("cerrar") else 200
        return JsonResponse({"status": "success", "data": resultado}, status=status_code)
    except ValidationError as exc:
        return JsonResponse({"status": "error", "message": str(exc)}, status=400)
    except Exception as exc:
        return JsonResponse({"status": "error", "message": str(exc)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def listar_templates(request):
    """Lista templates de expensa.

    GET: /api/expensas/templates/?consorcio=<cuit>
    """

    try:
        consorcio = request.GET.get("consorcio")
        queryset = ExpensaTemplate.objects.all()
        if consorcio:
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
        return JsonResponse({"status": "success", "data": templates})
    except Exception as exc:
        return JsonResponse({"status": "error", "message": str(exc)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def listar_templates_por_consorcio(request, cuit_consorcio):
    """Lista templates de expensa por consorcio."""
    try:
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
        return JsonResponse({"status": "success", "data": templates})
    except Exception as exc:
        return JsonResponse({"status": "error", "message": str(exc)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def crear_template(request):
    """Crea un template de expensa."""

    try:
        payload = json.loads(request.body)
        template = ExpensaTemplate.objects.create(
            consorcio_id=payload.get("consorcio"),
            nombre=payload.get("nombre"),
            version=payload.get("version", 1),
            config=payload.get("config", {}),
            activo=payload.get("activo", True),
        )
        return JsonResponse(
            {
                "status": "success",
                "data": {
                    "id": template.id_expensa_template,
                    "consorcio": template.consorcio_id,
                    "nombre": template.nombre,
                    "version": template.version,
                    "activo": template.activo,
                },
            },
            status=201,
        )
    except Exception as exc:
        return JsonResponse({"status": "error", "message": str(exc)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def obtener_template(request, template_id):
    """Obtiene un template de expensa por ID."""

    try:
        template = ExpensaTemplate.objects.get(pk=template_id)
        return JsonResponse(
            {
                "status": "success",
                "data": {
                    "id": template.id_expensa_template,
                    "consorcio": template.consorcio_id,
                    "nombre": template.nombre,
                    "version": template.version,
                    "activo": template.activo,
                    "config": template.config,
                },
            }
        )
    except ExpensaTemplate.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Template no encontrado."}, status=404)
    except Exception as exc:
        return JsonResponse({"status": "error", "message": str(exc)}, status=500)


@csrf_exempt
@require_http_methods(["PUT"])
def actualizar_template(request, template_id):
    """Actualiza un template de expensa."""

    try:
        payload = json.loads(request.body)
        template = ExpensaTemplate.objects.get(pk=template_id)
        for field in ["consorcio", "nombre", "version", "config", "activo"]:
            if field in payload:
                if field == "consorcio":
                    template.consorcio_id = payload[field]
                else:
                    setattr(template, field, payload[field])
        template.save()
        return JsonResponse(
            {
                "status": "success",
                "data": {
                    "id": template.id_expensa_template,
                    "consorcio": template.consorcio_id,
                    "nombre": template.nombre,
                    "version": template.version,
                    "activo": template.activo,
                    "config": template.config,
                },
            }
        )
    except ExpensaTemplate.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Template no encontrado."}, status=404)
    except Exception as exc:
        return JsonResponse({"status": "error", "message": str(exc)}, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def eliminar_template(request, template_id):
    """Elimina un template de expensa."""

    try:
        template = ExpensaTemplate.objects.get(pk=template_id)
        template.delete()
        return JsonResponse({"status": "success", "message": "Template eliminado."})
    except ExpensaTemplate.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Template no encontrado."}, status=404)
    except Exception as exc:
        return JsonResponse({"status": "error", "message": str(exc)}, status=500)
