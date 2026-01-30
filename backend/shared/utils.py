"""Utilidades compartidas para validaciones y enmascarado.

Fecha:
    27 - 01 - 2026
"""

from __future__ import annotations

from decimal import Decimal
import re
from typing import Iterable, Tuple

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

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
