"""Views para la app gastos.

Fecha:
    31 - 01 - 2026
"""

from datetime import datetime
from decimal import Decimal, InvalidOperation

from django.core.exceptions import ValidationError
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from shared.api_responses import exception_response, success_response, validation_error_response
from shared.auth import ensure_consorcio_access, filter_queryset_by_consorcios, get_request_user

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
        usuario_autenticado = get_request_user(request)
        datos = json.loads(request.body)
        if "consorcio" in datos:
            datos["consorcio_id"] = datos.pop("consorcio")
        if "proveedor" in datos:
            datos["proveedor_id"] = datos.pop("proveedor")
        ensure_consorcio_access(usuario_autenticado, datos.get("consorcio_id"))
        gasto = GastoService.crear_gasto(datos)
        return success_response({
            "id": gasto.id_gasto,
            "monto": str(gasto.monto),
        }, message="Gasto creado exitosamente", status=201)
    except Exception as e:
        return exception_response(e, validation_message="Error de validación al crear gasto.")


@csrf_exempt
@require_http_methods(["GET"])
def obtener_gasto(request, id_gasto):
    """Obtiene un gasto específico."""
    try:
        usuario_autenticado = get_request_user(request)
        gasto = GastoService.obtener_gasto(id_gasto)
        ensure_consorcio_access(usuario_autenticado, gasto.consorcio_id)
        return success_response({
            "id": gasto.id_gasto,
            "consorcio": str(gasto.consorcio.cuit),
            "proveedor": str(gasto.proveedor.cuit),
            "periodo": str(gasto.periodo),
            "descripcion": gasto.descripcion,
            "monto": str(gasto.monto),
            "fecha_registro": gasto.fecha_registro.isoformat(),
            "tipo_gasto": gasto.tipo_gasto,
            "estado_pago": gasto.estado_pago,
        })
    except Exception as e:
        return exception_response(e, not_found_message="Gasto no encontrado.")


@csrf_exempt
@require_http_methods(["GET"])
def listar_gastos(request):
    """Lista todos los gastos."""
    try:
        usuario_autenticado = get_request_user(request)
        gastos = filter_queryset_by_consorcios(GastoService.listar_gastos(), usuario_autenticado)
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
        return success_response(datos, count=len(datos))
    except Exception as e:
        return exception_response(e)


@csrf_exempt
@require_http_methods(["GET"])
def listar_gastos_por_consorcio(request, cuit_consorcio):
    """Lista gastos de un consorcio."""
    try:
        usuario_autenticado = get_request_user(request)
        ensure_consorcio_access(usuario_autenticado, cuit_consorcio)
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
        return success_response(datos, count=len(datos))
    except Exception as e:
        return exception_response(e)


@csrf_exempt
@require_http_methods(["GET"])
def listar_gastos_por_proveedor(request, cuit_proveedor):
    """Lista gastos de un proveedor."""
    try:
        usuario_autenticado = get_request_user(request)
        gastos = filter_queryset_by_consorcios(
            GastoService.listar_gastos_por_proveedor(cuit_proveedor),
            usuario_autenticado,
        )
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
        return success_response(datos, count=len(datos))
    except Exception as e:
        return exception_response(e)


@csrf_exempt
@require_http_methods(["GET"])
def listar_gastos_por_tipo(request, tipo_gasto):
    """Lista gastos por tipo."""
    try:
        usuario_autenticado = get_request_user(request)
        gastos = filter_queryset_by_consorcios(
            GastoService.listar_gastos_por_tipo(tipo_gasto),
            usuario_autenticado,
        )
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
        return success_response(datos, count=len(datos))
    except Exception as e:
        return exception_response(e)


@csrf_exempt
@require_http_methods(["GET"])
def listar_gastos_por_estado(request, estado_pago):
    """Lista gastos por estado de pago."""
    try:
        usuario_autenticado = get_request_user(request)
        gastos = filter_queryset_by_consorcios(
            GastoService.listar_gastos_por_estado(estado_pago),
            usuario_autenticado,
        )
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
        usuario_autenticado = get_request_user(request)
        gasto_actual = GastoService.obtener_gasto(id_gasto)
        ensure_consorcio_access(usuario_autenticado, gasto_actual.consorcio_id)

        datos = json.loads(request.body)
        if "consorcio" in datos:
            datos["consorcio_id"] = datos.pop("consorcio")
        if "proveedor" in datos:
            datos["proveedor_id"] = datos.pop("proveedor")
        if datos.get("consorcio_id"):
            ensure_consorcio_access(usuario_autenticado, datos.get("consorcio_id"))
        gasto = GastoService.actualizar_gasto(id_gasto, datos)
        return success_response({
            "id": gasto.id_gasto,
            "monto": str(gasto.monto),
        }, message="Gasto actualizado exitosamente")
    except Exception as e:
        return exception_response(
            e,
            validation_message="Error de validación al actualizar gasto.",
            not_found_message="Gasto no encontrado.",
        )


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
        usuario_autenticado = get_request_user(request)
        archivo = request.FILES.get("archivo")
        if not archivo:
            return validation_error_response(
                "Error de validación al procesar el archivo.",
                ValidationError({"archivo": ["No se proporcionó ningún archivo."]}),
            )

        extraidos = process_file(archivo)

        consorcio = request.POST.get("consorcio")
        proveedor = request.POST.get("proveedor") or extraidos.get("cuit_proveedor")
        periodo = request.POST.get("periodo") or extraidos.get("periodo_facturado") or extraidos.get("fecha")
        descripcion = request.POST.get("descripcion") or extraidos.get("descripcion")
        monto = request.POST.get("monto") or extraidos.get("importe_total")
        tipo_gasto = request.POST.get("tipo_gasto")
        estado_pago = request.POST.get("estado_pago")

        if not consorcio:
            return validation_error_response(
                "Error de validación al crear gasto desde archivo.",
                ValidationError({"consorcio": ["El campo consorcio es obligatorio."]}),
            )
        ensure_consorcio_access(usuario_autenticado, consorcio)
        if not proveedor:
            return validation_error_response(
                "Error de validación al crear gasto desde archivo.",
                ValidationError({"proveedor": ["No se pudo determinar el proveedor."]}),
            )
        if not monto:
            return validation_error_response(
                "Error de validación al crear gasto desde archivo.",
                ValidationError({"monto": ["No se pudo determinar el monto."]}),
            )
        if not periodo:
            return validation_error_response(
                "Error de validación al crear gasto desde archivo.",
                ValidationError({"periodo": ["No se pudo determinar el periodo."]}),
            )

        try:
            monto_normalizado = str(monto).replace(".", "").replace(",", ".")
            monto_decimal = Decimal(monto_normalizado)
        except (InvalidOperation, AttributeError):
            return validation_error_response(
                "Error de validación al crear gasto desde archivo.",
                ValidationError({"monto": ["El monto no es válido."]}),
            )

        try:
            if isinstance(periodo, str) and "/" in periodo and len(periodo) == 7:
                periodo_fecha = datetime.strptime(periodo, "%m/%Y").date().replace(day=1)
            elif isinstance(periodo, str) and "/" in periodo and len(periodo) == 10:
                periodo_fecha = datetime.strptime(periodo, "%d/%m/%Y").date()
            else:
                periodo_fecha = datetime.strptime(periodo, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            return validation_error_response(
                "Error de validación al crear gasto desde archivo.",
                ValidationError({"periodo": ["El periodo no tiene un formato válido."]}),
            )

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

        return success_response({
            "id": gasto.id_gasto,
            "monto": str(gasto.monto),
        }, message="Gasto creado exitosamente desde el archivo.", status=201)
    except Exception as e:
        return exception_response(e, validation_message="Error de validación al crear gasto desde archivo.")


@csrf_exempt
@require_http_methods(["POST"])
def extraer_gasto_desde_archivo(request):
    """Extrae datos de un archivo (pdf o imagen) sin crear el gasto."""
    try:
        get_request_user(request)
        archivo = request.FILES.get("archivo")
        if not archivo:
            return validation_error_response(
                "Error de validación al extraer datos del archivo.",
                ValidationError({"archivo": ["No se proporcionó ningún archivo."]}),
            )

        extraidos = process_file(archivo)
        periodo = extraidos.get("periodo_facturado") or extraidos.get("fecha")
        return success_response({
            "cuit_proveedor": extraidos.get("cuit_proveedor"),
            "periodo": periodo,
            "descripcion": extraidos.get("descripcion"),
            "monto": extraidos.get("importe_total"),
            "raw_text": extraidos.get("raw_text"),
        })
    except Exception as e:
        return exception_response(e, validation_message="Error de validación al extraer datos del archivo.")


@csrf_exempt
@require_http_methods(["DELETE"])
def eliminar_gasto(request, id_gasto):
    """Elimina un gasto."""
    try:
        usuario_autenticado = get_request_user(request)
        gasto = GastoService.obtener_gasto(id_gasto)
        ensure_consorcio_access(usuario_autenticado, gasto.consorcio_id)
        GastoService.eliminar_gasto(id_gasto)
        return success_response(message="Gasto eliminado exitosamente")
    except Exception as e:
        return exception_response(e, not_found_message="Gasto no encontrado.")
