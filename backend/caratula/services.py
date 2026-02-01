"""Servicios para la app caratula.

Fecha:
    31 - 01 - 2026
"""

from django.core.exceptions import ValidationError
from .models import Caratula


class CaratulaService:
    """Servicio para gestionar operaciones CRUD de Carátulas."""

    @staticmethod
    def crear_caratula(datos: dict) -> Caratula:
        """Crea una nueva carátula.

        Args:
            datos (dict): Datos de la carátula.

        Returns:
            Caratula: Instancia creada.

        Raises:
            ValidationError: Si los datos son inválidos.
        """
        try:
            caratula = Caratula(**datos)
            caratula.full_clean()
            caratula.save()
            return caratula
        except ValidationError as e:
            raise ValidationError(f"Error al crear carátula: {e.messages}")

    @staticmethod
    def obtener_caratula(fecha_caratula):
        """Obtiene una carátula por fecha.

        Args:
            fecha_caratula: Fecha de la carátula.

        Returns:
            Caratula: Carátula encontrada.

        Raises:
            Caratula.DoesNotExist: Si no existe.
        """
        return Caratula.objects.get(pk=fecha_caratula)

    @staticmethod
    def listar_caratulas():
        """Lista todas las carátulas.

        Returns:
            QuerySet: Todas las carátulas.
        """
        return Caratula.objects.all()

    @staticmethod
    def listar_caratulas_por_consorcio(cuit_consorcio: str):
        """Lista carátulas de un consorcio.

        Args:
            cuit_consorcio (str): CUIT del consorcio.

        Returns:
            QuerySet: Carátulas del consorcio.
        """
        return Caratula.objects.filter(consorcio_id=cuit_consorcio)

    @staticmethod
    def actualizar_caratula(fecha_caratula, datos: dict) -> Caratula:
        """Actualiza una carátula.

        Args:
            fecha_caratula: Fecha de la carátula.
            datos (dict): Datos a actualizar.

        Returns:
            Caratula: Carátula actualizada.

        Raises:
            ValidationError: Si los datos son inválidos.
            Caratula.DoesNotExist: Si no existe.
        """
        try:
            caratula = Caratula.objects.get(pk=fecha_caratula)
            for key, value in datos.items():
                if hasattr(caratula, key):
                    setattr(caratula, key, value)
            caratula.full_clean()
            caratula.save()
            return caratula
        except ValidationError as e:
            raise ValidationError(f"Error al actualizar carátula: {e.messages}")

    @staticmethod
    def eliminar_caratula(fecha_caratula) -> None:
        """Elimina una carátula.

        Args:
            fecha_caratula: Fecha de la carátula.

        Raises:
            Caratula.DoesNotExist: Si no existe.
        """
        caratula = Caratula.objects.get(pk=fecha_caratula)
        caratula.delete()
