"""Servicios para la app pagos.

Fecha:
    31 - 01 - 2026
"""

from django.core.exceptions import ValidationError
from .models import Pago


class PagoService:
    """Servicio para gestionar operaciones CRUD de Pagos."""

    @staticmethod
    def crear_pago(datos: dict) -> Pago:
        """Crea un nuevo pago.

        Args:
            datos (dict): Datos del pago.

        Returns:
            Pago: Instancia creada.

        Raises:
            ValidationError: Si los datos son inválidos.
        """
        try:
            pago = Pago(**datos)
            pago.full_clean()
            pago.save()
            return pago
        except ValidationError as e:
            raise ValidationError(f"Error al crear pago: {e.messages}")

    @staticmethod
    def obtener_pago(id_pago: int) -> Pago:
        """Obtiene un pago por ID.

        Args:
            id_pago (int): ID del pago.

        Returns:
            Pago: Pago encontrado.

        Raises:
            Pago.DoesNotExist: Si no existe.
        """
        return Pago.objects.get(pk=id_pago)

    @staticmethod
    def listar_pagos():
        """Lista todos los pagos.

        Returns:
            QuerySet: Todos los pagos.
        """
        return Pago.objects.all()

    @staticmethod
    def listar_pagos_por_consorcio(cuit_consorcio: str):
        """Lista pagos de un consorcio.

        Args:
            cuit_consorcio (str): CUIT del consorcio.

        Returns:
            QuerySet: Pagos del consorcio.
        """
        return Pago.objects.filter(consorcio_id=cuit_consorcio)

    @staticmethod
    def listar_pagos_por_propietario(dni_propietario: str):
        """Lista pagos de un propietario.

        Args:
            dni_propietario (str): DNI del propietario.

        Returns:
            QuerySet: Pagos del propietario.
        """
        return Pago.objects.filter(propietario_id=dni_propietario)

    @staticmethod
    def listar_pagos_por_unidad_funcional(numero_unidad: int):
        """Lista pagos de una unidad funcional.

        Args:
            numero_unidad (int): Número de la unidad funcional.

        Returns:
            QuerySet: Pagos de la unidad funcional.
        """
        return Pago.objects.filter(numero_de_unidad_funcional=numero_unidad)

    @staticmethod
    def actualizar_pago(id_pago: int, datos: dict) -> Pago:
        """Actualiza un pago.

        Args:
            id_pago (int): ID del pago.
            datos (dict): Datos a actualizar.

        Returns:
            Pago: Pago actualizado.

        Raises:
            ValidationError: Si los datos son inválidos.
            Pago.DoesNotExist: Si no existe.
        """
        try:
            pago = Pago.objects.get(pk=id_pago)
            for key, value in datos.items():
                if hasattr(pago, key):
                    setattr(pago, key, value)
            pago.full_clean()
            pago.save()
            return pago
        except ValidationError as e:
            raise ValidationError(f"Error al actualizar pago: {e.messages}")

    @staticmethod
    def eliminar_pago(id_pago: int) -> None:
        """Elimina un pago.

        Args:
            id_pago (int): ID del pago.

        Raises:
            Pago.DoesNotExist: Si no existe.
        """
        pago = Pago.objects.get(pk=id_pago)
        pago.delete()
