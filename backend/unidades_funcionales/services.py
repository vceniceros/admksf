"""Servicios para la app unidades_funcionales.

Fecha:
    31 - 01 - 2026
"""

from django.core.exceptions import ValidationError
from .models import UnidadFuncional


class UnidadFuncionalService:
    """Servicio para gestionar operaciones CRUD de Unidades Funcionales."""

    @staticmethod
    def crear_unidad_funcional(datos: dict) -> UnidadFuncional:
        """Crea una nueva unidad funcional.

        Args:
            datos (dict): Datos de la unidad funcional.

        Returns:
            UnidadFuncional: Instancia creada.

        Raises:
            ValidationError: Si los datos son inválidos.
        """
        try:
            unidad = UnidadFuncional(**datos)
            unidad.full_clean()
            unidad.save()
            return unidad
        except ValidationError as e:
            raise ValidationError(f"Error al crear unidad funcional: {e.messages}")

    @staticmethod
    def obtener_unidad_funcional(numero: int) -> UnidadFuncional:
        """Obtiene una unidad funcional por número.

        Args:
            numero (int): Número de la unidad funcional.

        Returns:
            UnidadFuncional: Unidad funcional encontrada.

        Raises:
            UnidadFuncional.DoesNotExist: Si no existe.
        """
        return UnidadFuncional.objects.get(pk=numero)

    @staticmethod
    def listar_unidades_funcionales():
        """Lista todas las unidades funcionales.

        Returns:
            QuerySet: Todas las unidades funcionales.
        """
        return UnidadFuncional.objects.all()

    @staticmethod
    def listar_unidades_por_consorcio(cuit_consorcio: str):
        """Lista unidades funcionales de un consorcio.

        Args:
            cuit_consorcio (str): CUIT del consorcio.

        Returns:
            QuerySet: Unidades funcionales del consorcio.
        """
        return UnidadFuncional.objects.filter(consorcio_id=cuit_consorcio)

    @staticmethod
    def listar_unidades_por_propietario(dni_propietario: str):
        """Lista unidades funcionales de un propietario.

        Args:
            dni_propietario (str): DNI del propietario.

        Returns:
            QuerySet: Unidades funcionales del propietario.
        """
        return UnidadFuncional.objects.filter(propietario_id=dni_propietario)

    @staticmethod
    def actualizar_unidad_funcional(numero: int, datos: dict) -> UnidadFuncional:
        """Actualiza una unidad funcional.

        Args:
            numero (int): Número de la unidad funcional.
            datos (dict): Datos a actualizar.

        Returns:
            UnidadFuncional: Unidad funcional actualizada.

        Raises:
            ValidationError: Si los datos son inválidos.
            UnidadFuncional.DoesNotExist: Si no existe.
        """
        try:
            unidad = UnidadFuncional.objects.get(pk=numero)
            for key, value in datos.items():
                if hasattr(unidad, key):
                    setattr(unidad, key, value)
            unidad.full_clean()
            unidad.save()
            return unidad
        except ValidationError as e:
            raise ValidationError(f"Error al actualizar unidad funcional: {e.messages}")

    @staticmethod
    def eliminar_unidad_funcional(numero: int) -> None:
        """Elimina una unidad funcional.

        Args:
            numero (int): Número de la unidad funcional.

        Raises:
            UnidadFuncional.DoesNotExist: Si no existe.
        """
        unidad = UnidadFuncional.objects.get(pk=numero)
        unidad.delete()
