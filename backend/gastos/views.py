"""Views para la app gastos.

Fecha:
    31 - 01 - 2026
"""

from datetime import datetime
from decimal import Decimal, InvalidOperation

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from .services import GastoService
from shared.utils import process_file


@csrf_exempt
@require_http_methods(["POST"])
def crear_gasto(request):
    """Crea un nuevo gasto.
    
    POST: {
        "consorcio": "string (cuit)",
        "proveedor": "string (cuit)",
        "periodo": "date",
        "descripcion": "string",
        "monto": "decimal",
        "tipo_gasto": "string",
        "estado_pago": "string"
    }
    """
    try:
        datos = json.loads(request.body)
        if "consorcio" in datos:
            datos["consorcio_id"] = datos.pop("consorcio")
        if "proveedor" in datos:
            datos["proveedor_id"] = datos.pop("proveedor")
        gasto = GastoService.crear_gasto(datos)
        return JsonResponse({
            "status": "success",
            "message": "Gasto creado exitosamente",
            "data": {
                "id": gasto.id_gasto,
                "monto": str(gasto.monto),
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
def obtener_gasto(request, id_gasto):
    """Obtiene un gasto específico."""
    try:
        gasto = GastoService.obtener_gasto(id_gasto)
        return JsonResponse({
            "status": "success",
            "data": {
                "id": gasto.id_gasto,
                "consorcio": str(gasto.consorcio.cuit),
                "proveedor": str(gasto.proveedor.cuit),
                "periodo": str(gasto.periodo),
                "descripcion": gasto.descripcion,
                "monto": str(gasto.monto),
                "fecha_registro": gasto.fecha_registro.isoformat(),
                "tipo_gasto": gasto.tipo_gasto,
                "estado_pago": gasto.estado_pago,
            }
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": f"Gasto no encontrado: {str(e)}",
        }, status=404)


@csrf_exempt
@require_http_methods(["GET"])
def listar_gastos(request):
    """Lista todos los gastos."""
    try:
        gastos = GastoService.listar_gastos()
        datos = [{
            "id": g.id_gasto,
            "consorcio": str(g.consorcio.cuit),
            "proveedor": str(g.proveedor.cuit),
            "periodo": str(g.periodo),
            "descripcion": g.descripcion,
            "monto": str(g.monto),
            "fecha_registro": g.fecha_registro.isoformat(),
            "tipo_gasto": g.tipo_gasto,
            "estado_pago": g.estado_pago,
        } for g in gastos]
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
def listar_gastos_por_consorcio(request, cuit_consorcio):
    """Lista gastos de un consorcio."""
    try:
        gastos = GastoService.listar_gastos_por_consorcio(cuit_consorcio)
        datos = [{
            "id": g.id_gasto,
            "consorcio": str(g.consorcio.cuit),
            "proveedor": str(g.proveedor.cuit),
            "periodo": str(g.periodo),
            "descripcion": g.descripcion,
            "monto": str(g.monto),
            "tipo_gasto": g.tipo_gasto,
            "estado_pago": g.estado_pago,
            "fecha_registro": g.fecha_registro.isoformat(),
        } for g in gastos]
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
def listar_gastos_por_proveedor(request, cuit_proveedor):
    """Lista gastos de un proveedor."""
    try:
        gastos = GastoService.listar_gastos_por_proveedor(cuit_proveedor)
        datos = [{
            "id": g.id_gasto,
            "consorcio": str(g.consorcio.cuit),
            "proveedor": str(g.proveedor.cuit),
            "periodo": str(g.periodo),
            "descripcion": g.descripcion,
            "monto": str(g.monto),
            "tipo_gasto": g.tipo_gasto,
            "estado_pago": g.estado_pago,
            "fecha_registro": g.fecha_registro.isoformat(),
        } for g in gastos]
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
def listar_gastos_por_tipo(request, tipo_gasto):
    """Lista gastos por tipo."""
    try:
        gastos = GastoService.listar_gastos_por_tipo(tipo_gasto)
        datos = [{
            "id": g.id_gasto,
            "consorcio": str(g.consorcio.cuit),
            "proveedor": str(g.proveedor.cuit),
            "periodo": str(g.periodo),
            "descripcion": g.descripcion,
            "monto": str(g.monto),
            "tipo_gasto": g.tipo_gasto,
            "estado_pago": g.estado_pago,
            "fecha_registro": g.fecha_registro.isoformat(),
        } for g in gastos]
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
def listar_gastos_por_estado(request, estado_pago):
    """Lista gastos por estado de pago."""
    try:
        gastos = GastoService.listar_gastos_por_estado(estado_pago)
        datos = [{
            "id": g.id_gasto,
            "consorcio": str(g.consorcio.cuit),
            "proveedor": str(g.proveedor.cuit),
            "periodo": str(g.periodo),
            "descripcion": g.descripcion,
            "monto": str(g.monto),
            "estado_pago": g.estado_pago,
            "tipo_gasto": g.tipo_gasto,
            "fecha_registro": g.fecha_registro.isoformat(),
        } for g in gastos]
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
def actualizar_gasto(request, id_gasto):
    """Actualiza un gasto existente."""
    try:
        datos = json.loads(request.body)
        if "consorcio" in datos:
            datos["consorcio_id"] = datos.pop("consorcio")
        if "proveedor" in datos:
            datos["proveedor_id"] = datos.pop("proveedor")
        gasto = GastoService.actualizar_gasto(id_gasto, datos)
        return JsonResponse({
            "status": "success",
            "message": "Gasto actualizado exitosamente",
            "data": {
                "id": gasto.id_gasto,
                "monto": str(gasto.monto),
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
@require_http_methods(["POST"])
def cargar_gasto_desde_archivo(request):
    """Carga un gasto desde un archivo (pdf o imagen) y extrae datos relevantes.

    POST (multipart/form-data):
        archivo: archivo PDF o imagen
        consorcio: string (cuit) [requerido]
        proveedor: string (cuit) [opcional si viene en el archivo]
        periodo: date (YYYY-MM-DD) [opcional si se detecta del archivo]
        descripcion: string [opcional]
        monto: decimal [opcional si se detecta del archivo]
        tipo_gasto: string [opcional]
        estado_pago: string [opcional]
    """
    try:
        archivo = request.FILES.get("archivo")
        if not archivo:
            return JsonResponse({
                "status": "error",
                "message": "No se proporcionó ningún archivo.",
            }, status=400)

        extraidos = process_file(archivo)

        consorcio = request.POST.get("consorcio")
        proveedor = request.POST.get("proveedor") or extraidos.get("cuit_proveedor")
        periodo = request.POST.get("periodo") or extraidos.get("periodo_facturado") or extraidos.get("fecha")
        descripcion = request.POST.get("descripcion") or extraidos.get("descripcion")
        monto = request.POST.get("monto") or extraidos.get("importe_total")
        tipo_gasto = request.POST.get("tipo_gasto")
        estado_pago = request.POST.get("estado_pago")

        if not consorcio:
            return JsonResponse({
                "status": "error",
                "message": "El campo consorcio es obligatorio.",
            }, status=400)
        if not proveedor:
            return JsonResponse({
                "status": "error",
                "message": "No se pudo determinar el proveedor.",
            }, status=400)
        if not monto:
            return JsonResponse({
                "status": "error",
                "message": "No se pudo determinar el monto.",
            }, status=400)
        if not periodo:
            return JsonResponse({
                "status": "error",
                "message": "No se pudo determinar el periodo.",
            }, status=400)

        try:
            monto_normalizado = str(monto).replace(".", "").replace(",", ".")
            monto_decimal = Decimal(monto_normalizado)
        except (InvalidOperation, AttributeError):
            return JsonResponse({
                "status": "error",
                "message": "El monto no es válido.",
            }, status=400)

        try:
            if isinstance(periodo, str) and "/" in periodo and len(periodo) == 7:
                periodo_fecha = datetime.strptime(periodo, "%m/%Y").date().replace(day=1)
            elif isinstance(periodo, str) and "/" in periodo and len(periodo) == 10:
                periodo_fecha = datetime.strptime(periodo, "%d/%m/%Y").date()
            else:
                periodo_fecha = datetime.strptime(periodo, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            return JsonResponse({
                "status": "error",
                "message": "El periodo no tiene un formato válido.",
            }, status=400)

        datos_gasto = {
            "consorcio_id": consorcio,
            "proveedor_id": proveedor,
            "periodo": periodo_fecha,
            "descripcion": descripcion or "Gasto importado desde archivo",
            "monto": monto_decimal,
        }
        if tipo_gasto:
            datos_gasto["tipo_gasto"] = tipo_gasto
        if estado_pago:
            datos_gasto["estado_pago"] = estado_pago

        gasto = GastoService.crear_gasto(datos_gasto)

        return JsonResponse({
            "status": "success",
            "message": "Gasto creado exitosamente desde el archivo.",
            "data": {
                "id": gasto.id_gasto,
                "monto": str(gasto.monto),
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
@require_http_methods(["POST"])
def extraer_gasto_desde_archivo(request):
    """Extrae datos de un archivo (pdf o imagen) sin crear el gasto."""
    try:
        archivo = request.FILES.get("archivo")
        if not archivo:
            return JsonResponse({
                "status": "error",
                "message": "No se proporcionó ningún archivo.",
            }, status=400)

        extraidos = process_file(archivo)
        periodo = extraidos.get("periodo_facturado") or extraidos.get("fecha")
        return JsonResponse({
            "status": "success",
            "data": {
                "cuit_proveedor": extraidos.get("cuit_proveedor"),
                "periodo": periodo,
                "descripcion": extraidos.get("descripcion"),
                "monto": extraidos.get("importe_total"),
                "raw_text": extraidos.get("raw_text"),
            }
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e),
        }, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def eliminar_gasto(request, id_gasto):
    """Elimina un gasto."""
    try:
        GastoService.eliminar_gasto(id_gasto)
        return JsonResponse({
            "status": "success",
            "message": "Gasto eliminado exitosamente",
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e),
        }, status=404)
