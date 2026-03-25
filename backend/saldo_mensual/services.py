"""Servicios para la app saldo_mensual.

Fecha:
    31 - 01 - 2026
"""

from django.core.exceptions import ValidationError
from .models import SaldoMensual


class SaldoMensualService:
    """Servicio para gestionar operaciones CRUD de Saldos Mensuales."""

    @staticmethod
    def crear_saldo_mensual(datos: dict) -> SaldoMensual:
        """Crea un nuevo saldo mensual.

        Args:
            datos (dict): Datos del saldo mensual.

        Returns:
            SaldoMensual: Instancia creada.

        Raises:
            ValidationError: Si los datos son inválidos.
        """
        try:
            saldo = SaldoMensual(**datos)
            saldo.full_clean()
            saldo.save()
            return saldo
        except ValidationError as e:
            raise ValidationError(f"Error al crear saldo mensual: {e.messages}")

    @staticmethod
    def obtener_saldo_mensual(id_saldo: int) -> SaldoMensual:
        """Obtiene un saldo mensual por ID.

        Args:
            id_saldo (int): ID del saldo mensual.

        Returns:
            SaldoMensual: Saldo mensual encontrado.

        Raises:
            SaldoMensual.DoesNotExist: Si no existe.
        """
        return SaldoMensual.objects.get(pk=id_saldo)

    @staticmethod
    def listar_saldos_mensuales():
        """Lista todos los saldos mensuales.

        Returns:
            QuerySet: Todos los saldos mensuales.
        """
        return SaldoMensual.objects.all()

    @staticmethod
    def listar_saldos_por_consorcio(cuit_consorcio: str):
        """Lista saldos mensuales de un consorcio.

        Args:
            cuit_consorcio (str): CUIT del consorcio.

        Returns:
            QuerySet: Saldos mensuales del consorcio.
        """
        return SaldoMensual.objects.filter(consorcio_id=cuit_consorcio)

    @staticmethod
    def listar_saldos_por_unidad_funcional(numero_unidad: int):
        """Lista saldos mensuales de una unidad funcional.

        Args:
            numero_unidad (int): Número de la unidad funcional.

        Returns:
            QuerySet: Saldos mensuales de la unidad funcional.
        """
        return SaldoMensual.objects.filter(numero_de_unidad_funcional=numero_unidad)

    @staticmethod
    def actualizar_saldo_mensual(id_saldo: int, datos: dict) -> SaldoMensual:
        """Actualiza un saldo mensual.

        Args:
            id_saldo (int): ID del saldo mensual.
            datos (dict): Datos a actualizar.

        Returns:
            SaldoMensual: Saldo mensual actualizado.

        Raises:
            ValidationError: Si los datos son inválidos.
            SaldoMensual.DoesNotExist: Si no existe.
        """
        try:
            saldo = SaldoMensual.objects.get(pk=id_saldo)
            for key, value in datos.items():
                if hasattr(saldo, key):
                    setattr(saldo, key, value)
            saldo.full_clean()
            saldo.save()
            return saldo
        except ValidationError as e:
            raise ValidationError(f"Error al actualizar saldo mensual: {e.messages}")

    @staticmethod
    def eliminar_saldo_mensual(id_saldo: int) -> None:
        """Elimina un saldo mensual.

        Args:
            id_saldo (int): ID del saldo mensual.

        Raises:
            SaldoMensual.DoesNotExist: Si no existe.
        """
        saldo = SaldoMensual.objects.get(pk=id_saldo)
        saldo.delete()
