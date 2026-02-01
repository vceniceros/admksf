"""Servicios para la app proveedores.

Fecha:
    31 - 01 - 2026
"""

from django.core.exceptions import ValidationError
from .models import Proveedor


class ProveedorService:
    """Servicio para gestionar operaciones CRUD de Proveedores."""

    @staticmethod
    def crear_proveedor(datos: dict) -> Proveedor:
        """Crea un nuevo proveedor.

        Args:
            datos (dict): Datos del proveedor.

        Returns:
            Proveedor: Instancia creada.

        Raises:
            ValidationError: Si los datos son inválidos.
        """
        try:
            proveedor = Proveedor(**datos)
            proveedor.full_clean()
            proveedor.save()
            return proveedor
        except ValidationError as e:
            raise ValidationError(f"Error al crear proveedor: {e.messages}")

    @staticmethod
    def obtener_proveedor(cuit: str) -> Proveedor:
        """Obtiene un proveedor por CUIT.

        Args:
            cuit (str): CUIT del proveedor.

        Returns:
            Proveedor: Proveedor encontrado.

        Raises:
            Proveedor.DoesNotExist: Si no existe.
        """
        return Proveedor.objects.get(pk=cuit)

    @staticmethod
    def listar_proveedores():
        """Lista todos los proveedores.

        Returns:
            QuerySet: Todos los proveedores.
        """
        return Proveedor.objects.all()

    @staticmethod
    def listar_proveedores_por_tipo(tipo_proveedor: str):
        """Lista proveedores por tipo.

        Args:
            tipo_proveedor (str): Tipo de proveedor.

        Returns:
            QuerySet: Proveedores del tipo especificado.
        """
        return Proveedor.objects.filter(tipo_proveedor=tipo_proveedor)

    @staticmethod
    def actualizar_proveedor(cuit: str, datos: dict) -> Proveedor:
        """Actualiza un proveedor.

        Args:
            cuit (str): CUIT del proveedor.
            datos (dict): Datos a actualizar.

        Returns:
            Proveedor: Proveedor actualizado.

        Raises:
            ValidationError: Si los datos son inválidos.
            Proveedor.DoesNotExist: Si no existe.
        """
        try:
            proveedor = Proveedor.objects.get(pk=cuit)
            for key, value in datos.items():
                if hasattr(proveedor, key):
                    setattr(proveedor, key, value)
            proveedor.full_clean()
            proveedor.save()
            return proveedor
        except ValidationError as e:
            raise ValidationError(f"Error al actualizar proveedor: {e.messages}")

    @staticmethod
    def eliminar_proveedor(cuit: str) -> None:
        """Elimina un proveedor.

        Args:
            cuit (str): CUIT del proveedor.

        Raises:
            Proveedor.DoesNotExist: Si no existe.
        """
        proveedor = Proveedor.objects.get(pk=cuit)
        proveedor.delete()
