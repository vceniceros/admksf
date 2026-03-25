"""Servicios para la app gastos.

Fecha:
    31 - 01 - 2026
"""

from django.core.exceptions import ValidationError
from .models import Gasto


class GastoService:
    """Servicio para gestionar operaciones CRUD de Gastos."""

    @staticmethod
    def crear_gasto(datos: dict) -> Gasto:
        """Crea un nuevo gasto.

        Args:
            datos (dict): Datos del gasto.

        Returns:
            Gasto: Instancia creada.

        Raises:
            ValidationError: Si los datos son inválidos.
        """
        try:
            gasto = Gasto(**datos)
            gasto.full_clean()
            gasto.save()
            return gasto
        except ValidationError as e:
            raise ValidationError(f"Error al crear gasto: {e.messages}")

    @staticmethod
    def obtener_gasto(id_gasto: int) -> Gasto:
        """Obtiene un gasto por ID.

        Args:
            id_gasto (int): ID del gasto.

        Returns:
            Gasto: Gasto encontrado.

        Raises:
            Gasto.DoesNotExist: Si no existe.
        """
        return Gasto.objects.get(pk=id_gasto)

    @staticmethod
    def listar_gastos():
        """Lista todos los gastos.

        Returns:
            QuerySet: Todos los gastos.
        """
        return Gasto.objects.all()

    @staticmethod
    def listar_gastos_por_consorcio(cuit_consorcio: str):
        """Lista gastos de un consorcio.

        Args:
            cuit_consorcio (str): CUIT del consorcio.

        Returns:
            QuerySet: Gastos del consorcio.
        """
        return Gasto.objects.filter(consorcio_id=cuit_consorcio)

    @staticmethod
    def listar_gastos_por_proveedor(cuit_proveedor: str):
        """Lista gastos de un proveedor.

        Args:
            cuit_proveedor (str): CUIT del proveedor.

        Returns:
            QuerySet: Gastos del proveedor.
        """
        return Gasto.objects.filter(proveedor_id=cuit_proveedor)

    @staticmethod
    def listar_gastos_por_tipo(tipo_gasto: str):
        """Lista gastos por tipo.

        Args:
            tipo_gasto (str): Tipo de gasto.

        Returns:
            QuerySet: Gastos del tipo especificado.
        """
        return Gasto.objects.filter(tipo_gasto=tipo_gasto)

    @staticmethod
    def listar_gastos_por_estado(estado_pago: str):
        """Lista gastos por estado de pago.

        Args:
            estado_pago (str): Estado del pago.

        Returns:
            QuerySet: Gastos con el estado especificado.
        """
        return Gasto.objects.filter(estado_pago=estado_pago)

    @staticmethod
    def actualizar_gasto(id_gasto: int, datos: dict) -> Gasto:
        """Actualiza un gasto.

        Args:
            id_gasto (int): ID del gasto.
            datos (dict): Datos a actualizar.

        Returns:
            Gasto: Gasto actualizado.

        Raises:
            ValidationError: Si los datos son inválidos.
            Gasto.DoesNotExist: Si no existe.
        """
        try:
            gasto = Gasto.objects.get(pk=id_gasto)
            for key, value in datos.items():
                if hasattr(gasto, key):
                    setattr(gasto, key, value)
            gasto.full_clean()
            gasto.save()
            return gasto
        except ValidationError as e:
            raise ValidationError(f"Error al actualizar gasto: {e.messages}")

    @staticmethod
    def eliminar_gasto(id_gasto: int) -> None:
        """Elimina un gasto.

        Args:
            id_gasto (int): ID del gasto.

        Raises:
            Gasto.DoesNotExist: Si no existe.
        """
        gasto = Gasto.objects.get(pk=id_gasto)
        gasto.delete()
