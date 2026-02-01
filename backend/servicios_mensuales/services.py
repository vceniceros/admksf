"""Servicios para la app servicios_mensuales.

Fecha:
    31 - 01 - 2026
"""

from django.core.exceptions import ValidationError
from .models import ServicioMensual


class ServicioMensualService:
    """Servicio para gestionar operaciones CRUD de Servicios Mensuales."""

    @staticmethod
    def crear_servicio_mensual(datos: dict) -> ServicioMensual:
        """Crea un nuevo servicio mensual.

        Args:
            datos (dict): Datos del servicio mensual.

        Returns:
            ServicioMensual: Instancia creada.

        Raises:
            ValidationError: Si los datos son inválidos.
        """
        try:
            sm = ServicioMensual(**datos)
            sm.full_clean()
            sm.save()
            return sm
        except ValidationError as e:
            raise ValidationError(f"Error al crear servicio mensual: {e.messages}")

    @staticmethod
    def obtener_servicio_mensual(cuit_proveedor: str) -> ServicioMensual:
        """Obtiene un servicio mensual por CUIT del proveedor.

        Args:
            cuit_proveedor (str): CUIT del proveedor.

        Returns:
            ServicioMensual: Servicio mensual encontrado.

        Raises:
            ServicioMensual.DoesNotExist: Si no existe.
        """
        return ServicioMensual.objects.get(pk=cuit_proveedor)

    @staticmethod
    def listar_servicios_mensuales():
        """Lista todos los servicios mensuales.

        Returns:
            QuerySet: Todos los servicios mensuales.
        """
        return ServicioMensual.objects.all()

    @staticmethod
    def actualizar_servicio_mensual(cuit_proveedor: str, datos: dict) -> ServicioMensual:
        """Actualiza un servicio mensual.

        Args:
            cuit_proveedor (str): CUIT del proveedor.
            datos (dict): Datos a actualizar.

        Returns:
            ServicioMensual: Servicio mensual actualizado.

        Raises:
            ValidationError: Si los datos son inválidos.
            ServicioMensual.DoesNotExist: Si no existe.
        """
        try:
            sm = ServicioMensual.objects.get(pk=cuit_proveedor)
            for key, value in datos.items():
                if hasattr(sm, key):
                    setattr(sm, key, value)
            sm.full_clean()
            sm.save()
            return sm
        except ValidationError as e:
            raise ValidationError(f"Error al actualizar servicio mensual: {e.messages}")

    @staticmethod
    def eliminar_servicio_mensual(cuit_proveedor: str) -> None:
        """Elimina un servicio mensual.

        Args:
            cuit_proveedor (str): CUIT del proveedor.

        Raises:
            ServicioMensual.DoesNotExist: Si no existe.
        """
        sm = ServicioMensual.objects.get(pk=cuit_proveedor)
        sm.delete()
