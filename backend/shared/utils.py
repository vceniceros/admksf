"""Utilidades compartidas para validaciones y enmascarado.

Fecha:
    27 - 01 - 2026
"""

from __future__ import annotations

from decimal import Decimal
import io
import re
from typing import Iterable, Tuple

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from pdf2image import convert_from_bytes
from google.cloud import vision
from .constants import ERROR_PREFIX, MASK_CHAR, MASK_EMPTY_VALUE


def build_error_message(message: str) -> str:
    """Construye un mensaje de validación con prefijo fijo.

    Args:
        message (str): Mensaje base de error.

    Returns:
        str: Mensaje con prefijo de validación.
    """

    return f"{ERROR_PREFIX} {message}"


def digits_only_validator(field_label: str) -> RegexValidator:
    """Crea un validador de solo dígitos.

    Args:
        field_label (str): Nombre del campo para el mensaje.

    Returns:
        RegexValidator: Validador configurado.
    """

    return RegexValidator(
        regex=r"^\d+$",
        message=build_error_message(f"{field_label} debe contener solo dígitos."),
    )


def min_value_validator(min_value: Decimal | int | float, field_label: str) -> MinValueValidator:
    """Crea un validador de mínimo para un campo numérico.

    Args:
        min_value (Decimal | int | float): Valor mínimo permitido.
        field_label (str): Nombre del campo para el mensaje.

    Returns:
        MinValueValidator: Validador configurado.
    """

    return MinValueValidator(
        min_value,
        message=build_error_message(
            f"{field_label} debe ser mayor o igual a {min_value}."
        ),
    )


def max_value_validator(max_value: Decimal | int | float, field_label: str) -> MaxValueValidator:
    """Crea un validador de máximo para un campo numérico.

    Args:
        max_value (Decimal | int | float): Valor máximo permitido.
        field_label (str): Nombre del campo para el mensaje.

    Returns:
        MaxValueValidator: Validador configurado.
    """

    return MaxValueValidator(
        max_value,
        message=build_error_message(
            f"{field_label} debe ser menor o igual a {max_value}."
        ),
    )


def validate_regex_digits(value: str | None, field_label: str) -> None:
    """Valida que el valor contenga solo dígitos.

    Args:
        value (str | None): Valor a validar.
        field_label (str): Nombre del campo para el mensaje.

    Raises:
        ValidationError: Si el valor no cumple el patrón.
    """

    if value is None:
        return
    if not re.fullmatch(r"\d+", str(value)):
        raise ValidationError(build_error_message(f"{field_label} debe contener solo dígitos."))


def validate_min_value(
    value: Decimal | int | float | None,
    min_value: Decimal | int | float,
    field_label: str,
    inclusive: bool = True,
) -> None:
    """Valida un mínimo numérico.

    Args:
        value (Decimal | int | float | None): Valor a validar.
        min_value (Decimal | int | float): Límite mínimo.
        field_label (str): Nombre del campo para el mensaje.
        inclusive (bool): Si el límite es inclusivo.

    Raises:
        ValidationError: Si el valor está por debajo del mínimo.
    """

    if value is None:
        return
    if inclusive and value < min_value:
        raise ValidationError(build_error_message(f"{field_label} debe ser >= {min_value}."))
    if not inclusive and value <= min_value:
        raise ValidationError(build_error_message(f"{field_label} debe ser > {min_value}."))


def validate_max_value(
    value: Decimal | int | float | None,
    max_value: Decimal | int | float,
    field_label: str,
    inclusive: bool = True,
) -> None:
    """Valida un máximo numérico.

    Args:
        value (Decimal | int | float | None): Valor a validar.
        max_value (Decimal | int | float): Límite máximo.
        field_label (str): Nombre del campo para el mensaje.
        inclusive (bool): Si el límite es inclusivo.

    Raises:
        ValidationError: Si el valor supera el máximo.
    """

    if value is None:
        return
    if inclusive and value > max_value:
        raise ValidationError(build_error_message(f"{field_label} debe ser <= {max_value}."))
    if not inclusive and value >= max_value:
        raise ValidationError(build_error_message(f"{field_label} debe ser < {max_value}."))


def validate_range(
    value: Decimal | int | float | None,
    min_value: Decimal | int | float,
    max_value: Decimal | int | float,
    field_label: str,
) -> None:
    """Valida que el valor esté dentro de un rango inclusivo.

    Args:
        value (Decimal | int | float | None): Valor a validar.
        min_value (Decimal | int | float): Límite mínimo.
        max_value (Decimal | int | float): Límite máximo.
        field_label (str): Nombre del campo para el mensaje.

    Raises:
        ValidationError: Si el valor está fuera de rango.
    """

    validate_min_value(value, min_value, field_label, inclusive=True)
    validate_max_value(value, max_value, field_label, inclusive=True)


def validate_positive_decimal(value: Decimal | None, field_label: str) -> None:
    """Valida que el valor decimal sea estrictamente positivo.

    Args:
        value (Decimal | None): Valor a validar.
        field_label (str): Nombre del campo para el mensaje.

    Raises:
        ValidationError: Si el valor no es positivo.
    """

    validate_min_value(value, Decimal("0"), field_label, inclusive=False)


def validate_non_negative_decimal(value: Decimal | None, field_label: str) -> None:
    """Valida que el valor decimal sea no negativo.

    Args:
        value (Decimal | None): Valor a validar.
        field_label (str): Nombre del campo para el mensaje.

    Raises:
        ValidationError: Si el valor es negativo.
    """

    validate_min_value(value, Decimal("0"), field_label, inclusive=True)


def mask_value(value: object, keep_last: int = 4) -> str:
    """Enmascara un valor dejando solo los últimos caracteres visibles.

    Args:
        value (object): Valor a enmascarar.
        keep_last (int): Cantidad de caracteres visibles al final.

    Returns:
        str: Valor enmascarado.
    """

    if value is None:
        return MASK_EMPTY_VALUE
    string_value = str(value)
    if string_value == "":
        return MASK_EMPTY_VALUE
    if len(string_value) <= keep_last:
        return MASK_CHAR * len(string_value)
    masked = MASK_CHAR * (len(string_value) - keep_last)
    return f"{masked}{string_value[-keep_last:]}"


def format_field(name: str, value: object, mask: bool = False) -> str:
    """Formatea un campo para representación de texto.

    Args:
        name (str): Nombre del campo.
        value (object): Valor del campo.
        mask (bool): Indica si el valor debe enmascararse.

    Returns:
        str: Texto del campo formateado.
    """

    display_value = mask_value(value) if mask else value
    return f"{name}={display_value}"


def build_model_str(model_name: str, fields: Iterable[Tuple[str, object, bool]]) -> str:
    """Construye una representación de texto uniforme para un modelo.

    Args:
        model_name (str): Nombre del modelo.
        fields (Iterable[Tuple[str, object, bool]]): Campos con (nombre, valor, enmascarar).

    Returns:
        str: Representación en string del modelo.
    """

    parts = [format_field(name, value, mask) for name, value, mask in fields]
    return f"{model_name}({', '.join(parts)})"

def extract_text_from_img_by_vision(image_content: bytes) -> str:
    """Extrae texto de una imagen utilizando vision cloud ai de google cloud.

    Args:
        image_path (str): Ruta a la imagen.

    Returns:
        str: Texto extraído de la imagen.
    """
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)
    response = client.text_detection(image=image)

    if response.error.message:
        raise Exception(f"Error al procesar la imagen: {response.error.message}")
    if response.text_annotations:
        return response.text_annotations[0].description
    return ""


def parse_invoice_data(text: str) -> dict:
    """Parsea datos de una factura desde el texto extraído.

    Args:
        text (str): Texto extraído de la imagen.

    Returns:
        dict: Datos parseados de la factura.
    """
    data = {
        "raw_text": text,
        "fecha": None,
        "numero_factura": None,
        "importe_total": None,
        "cuit_proveedor": None,
        "periodo_facturado": None,
        "descripcion": None,
        "fecha_vencimiento": None,
    }

    fecha_match = re.search(r"Fecha[:\s]+(\d{2}/\d{2}/\d{4})", text, re.IGNORECASE)
    importe_match = re.search(r"(Total|Importe)[:\s]+\$?([\d.,]+)", text, re.IGNORECASE)
    cuit_match = re.search(r"CUIT[:\s]+(\d{2}-\d{8}-\d)", text, re.IGNORECASE)
    numero_factura_match = re.search(r"N(ro|ro\.|úmero|º)[:\s]+([\w-]+)", text, re.IGNORECASE)
    periodo_match = re.search(r"Periodo[:\s]+(\d{2}/\d{4})", text, re.IGNORECASE)
    fecha_vencimiento_match = re.search(r"Vencimiento[:\s]+(\d{2}/\d{2}/\d{4})", text, re.IGNORECASE)

    if fecha_match:
        data["fecha"] = fecha_match.group(1)
    if importe_match:
        data["importe_total"] = importe_match.group(2)
    if cuit_match:
        data["cuit_proveedor"] = cuit_match.group(1)
    if numero_factura_match:
        data["numero_factura"] = numero_factura_match.group(2)
    if periodo_match:
        data["periodo_facturado"] = periodo_match.group(1)
    if fecha_vencimiento_match:
        data["fecha_vencimiento"] = fecha_vencimiento_match.group(1)

    return data

def process_file(file_obj) -> dict:
    """Procesa un pdf o imagen y orquesta la estrategia de extracción de datos.

    Args:
        file_obj: Archivo a procesar.

    Returns:
        str: Contenido del archivo como texto.
    """
    file_bytes = file_obj.read()
    content_type = (file_obj.content_type or "").lower()
   
    full_text = ""
    if "pdf" in content_type:
        images = convert_from_bytes(file_bytes)
        if images:
            for image in images:
                image_buffer = io.BytesIO()
                image.save(image_buffer, format="JPEG")
                image_bytes = image_buffer.getvalue()
                full_text += extract_text_from_img_by_vision(image_bytes) + "\n"
    else:
        full_text = extract_text_from_img_by_vision(file_bytes)

    return parse_invoice_data(full_text)

