"""Servicios para la app consorcios.

Fecha:
    31 - 01 - 2026
"""

from django.core.exceptions import ValidationError
from django.db import transaction
from decimal import Decimal

from .models import Consorcio


class ConsorcioService:
    """Servicio para gestionar operaciones CRUD de Consorcios."""

    @staticmethod
    def crear_consorcio(datos: dict) -> Consorcio:
        """Crea un nuevo consorcio.

        Args:
            datos (dict): Datos del consorcio.

        Returns:
            Consorcio: Instancia creada.

        Raises:
            ValidationError: Si los datos son inválidos.
        """
        try:
            consorcio = Consorcio(**datos)
            consorcio.full_clean()
            consorcio.save()
            return consorcio
        except ValidationError as e:
            raise ValidationError(f"Error al crear consorcio: {e.messages}")

    @staticmethod
    def obtener_consorcio(cuit: str) -> Consorcio:
        """Obtiene un consorcio por CUIT.

        Args:
            cuit (str): CUIT del consorcio.

        Returns:
            Consorcio: Consorcio encontrado.

        Raises:
            Consorcio.DoesNotExist: Si no existe.
        """
        return Consorcio.objects.get(pk=cuit)

    @staticmethod
    def listar_consorcios():
        """Lista todos los consorcios.

        Returns:
            QuerySet: Todos los consorcios.
        """
        return Consorcio.objects.all()

    @staticmethod
    def actualizar_consorcio(cuit: str, datos: dict) -> Consorcio:
        """Actualiza un consorcio.

        Args:
            cuit (str): CUIT del consorcio.
            datos (dict): Datos a actualizar.

        Returns:
            Consorcio: Consorcio actualizado.

        Raises:
            ValidationError: Si los datos son inválidos.
            Consorcio.DoesNotExist: Si no existe.
        """
        try:
            consorcio = Consorcio.objects.get(pk=cuit)
            for key, value in datos.items():
                if hasattr(consorcio, key):
                    setattr(consorcio, key, value)
            consorcio.full_clean()
            consorcio.save()
            return consorcio
        except ValidationError as e:
            raise ValidationError(f"Error al actualizar consorcio: {e.messages}")

    @staticmethod
    def eliminar_consorcio(cuit: str) -> None:
        """Elimina un consorcio.

        Args:
            cuit (str): CUIT del consorcio.

        Raises:
            Consorcio.DoesNotExist: Si no existe.
        """
        consorcio = Consorcio.objects.get(pk=cuit)
        consorcio.delete()
