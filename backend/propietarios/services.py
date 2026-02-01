"""Servicios para la app propietarios.

Fecha:
    31 - 01 - 2026
"""

from django.core.exceptions import ValidationError
from .models import Propietario


class PropietarioService:
    """Servicio para gestionar operaciones CRUD de Propietarios."""

    @staticmethod
    def crear_propietario(datos: dict) -> Propietario:
        """Crea un nuevo propietario.

        Args:
            datos (dict): Datos del propietario.

        Returns:
            Propietario: Instancia creada.

        Raises:
            ValidationError: Si los datos son inválidos.
        """
        try:
            propietario = Propietario(**datos)
            propietario.full_clean()
            propietario.save()
            return propietario
        except ValidationError as e:
            raise ValidationError(f"Error al crear propietario: {e.messages}")

    @staticmethod
    def obtener_propietario(dni: str) -> Propietario:
        """Obtiene un propietario por DNI.

        Args:
            dni (str): DNI del propietario.

        Returns:
            Propietario: Propietario encontrado.

        Raises:
            Propietario.DoesNotExist: Si no existe.
        """
        return Propietario.objects.get(pk=dni)

    @staticmethod
    def listar_propietarios():
        """Lista todos los propietarios.

        Returns:
            QuerySet: Todos los propietarios.
        """
        return Propietario.objects.all()

    @staticmethod
    def actualizar_propietario(dni: str, datos: dict) -> Propietario:
        """Actualiza un propietario.

        Args:
            dni (str): DNI del propietario.
            datos (dict): Datos a actualizar.

        Returns:
            Propietario: Propietario actualizado.

        Raises:
            ValidationError: Si los datos son inválidos.
            Propietario.DoesNotExist: Si no existe.
        """
        try:
            propietario = Propietario.objects.get(pk=dni)
            for key, value in datos.items():
                if hasattr(propietario, key):
                    setattr(propietario, key, value)
            propietario.full_clean()
            propietario.save()
            return propietario
        except ValidationError as e:
            raise ValidationError(f"Error al actualizar propietario: {e.messages}")

    @staticmethod
    def eliminar_propietario(dni: str) -> None:
        """Elimina un propietario.

        Args:
            dni (str): DNI del propietario.

        Raises:
            Propietario.DoesNotExist: Si no existe.
        """
        propietario = Propietario.objects.get(pk=dni)
        propietario.delete()
