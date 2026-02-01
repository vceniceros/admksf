"""Servicios para la app reparaciones_mantenimientos.

Fecha:
    31 - 01 - 2026
"""

from django.core.exceptions import ValidationError
from .models import ReparacionMantenimiento


class ReparacionMantenimientoService:
    """Servicio para gestionar operaciones CRUD de Reparaciones y Mantenimientos."""

    @staticmethod
    def crear_reparacion_mantenimiento(datos: dict) -> ReparacionMantenimiento:
        """Crea un nuevo registro de reparación/mantenimiento.

        Args:
            datos (dict): Datos del registro.

        Returns:
            ReparacionMantenimiento: Instancia creada.

        Raises:
            ValidationError: Si los datos son inválidos.
        """
        try:
            rm = ReparacionMantenimiento(**datos)
            rm.full_clean()
            rm.save()
            return rm
        except ValidationError as e:
            raise ValidationError(f"Error al crear reparación/mantenimiento: {e.messages}")

    @staticmethod
    def obtener_reparacion_mantenimiento(cuit_proveedor: str) -> ReparacionMantenimiento:
        """Obtiene un registro por CUIT del proveedor.

        Args:
            cuit_proveedor (str): CUIT del proveedor.

        Returns:
            ReparacionMantenimiento: Registro encontrado.

        Raises:
            ReparacionMantenimiento.DoesNotExist: Si no existe.
        """
        return ReparacionMantenimiento.objects.get(pk=cuit_proveedor)

    @staticmethod
    def listar_reparaciones_mantenimientos():
        """Lista todos los registros de reparación/mantenimiento.

        Returns:
            QuerySet: Todos los registros.
        """
        return ReparacionMantenimiento.objects.all()

    @staticmethod
    def actualizar_reparacion_mantenimiento(cuit_proveedor: str, datos: dict) -> ReparacionMantenimiento:
        """Actualiza un registro de reparación/mantenimiento.

        Args:
            cuit_proveedor (str): CUIT del proveedor.
            datos (dict): Datos a actualizar.

        Returns:
            ReparacionMantenimiento: Registro actualizado.

        Raises:
            ValidationError: Si los datos son inválidos.
            ReparacionMantenimiento.DoesNotExist: Si no existe.
        """
        try:
            rm = ReparacionMantenimiento.objects.get(pk=cuit_proveedor)
            for key, value in datos.items():
                if hasattr(rm, key):
                    setattr(rm, key, value)
            rm.full_clean()
            rm.save()
            return rm
        except ValidationError as e:
            raise ValidationError(f"Error al actualizar reparación/mantenimiento: {e.messages}")

    @staticmethod
    def eliminar_reparacion_mantenimiento(cuit_proveedor: str) -> None:
        """Elimina un registro de reparación/mantenimiento.

        Args:
            cuit_proveedor (str): CUIT del proveedor.

        Raises:
            ReparacionMantenimiento.DoesNotExist: Si no existe.
        """
        rm = ReparacionMantenimiento.objects.get(pk=cuit_proveedor)
        rm.delete()
