"""Modelos de la app propietarios.

Fecha:
    27 - 01 - 2026
"""

from django.core.exceptions import ValidationError
from django.db import models

from shared import (
    build_model_str,
    digits_only_validator,
    validate_regex_digits,
)


class Propietario(models.Model):
    """Representa un propietario de unidades funcionales.

    Args:
        dni (str): DNI del propietario. Solo dígitos.
        nombre (str): Nombre.
        apellido (str): Apellido.
        telefono (str | None): Teléfono de contacto.
        email (str | None): Email de contacto.
    """

    dni = models.CharField(
        max_length=15,
        primary_key=True,
        db_column="dni",
        validators=[digits_only_validator("DNI")],
    )
    nombre = models.CharField(max_length=50, db_column="nombre")
    apellido = models.CharField(max_length=50, db_column="apellido")
    telefono = models.CharField(max_length=20, db_column="telefono", null=True, blank=True)
    email = models.EmailField(max_length=100, db_column="email", null=True, blank=True)

    class Meta:
        db_table = "propietarios"
        verbose_name = "Propietario"
        verbose_name_plural = "Propietarios"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(dni__regex=r"^\d+$"),
                name="propietarios_dni_solo_digitos",
            )
        ]

    def clean(self) -> None:
        """Valida reglas del propietario.

        Raises:
            ValidationError: Si el DNI no cumple el formato.
        """

        super().clean()
        validate_regex_digits(self.dni, "DNI")

    def __str__(self) -> str:
        """Devuelve una representación legible del propietario.

        Returns:
            str: Texto descriptivo del propietario.
        """

        return build_model_str(
            "Propietario",
            [
                ("dni", self.dni, True),
                ("nombre", self.nombre, False),
                ("apellido", self.apellido, False),
                ("telefono", self.telefono, True),
                ("email", self.email, True),
            ],
        )
