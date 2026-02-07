"""Servicios para la app consorcios.

Fecha:
    31 - 01 - 2026
"""

from django.core.exceptions import ValidationError
from decimal import Decimal
import re

from .models import Consorcio


class ConsorcioService:
    """Servicio para gestionar operaciones CRUD de Consorcios."""

    @staticmethod
    def _normalize_payload(datos: dict) -> dict:
        """Normaliza y limpia datos del consorcio."""
        if not isinstance(datos, dict):
            return {}

        cleaned = dict(datos)

        cuit = cleaned.get("cuit")
        if cuit is not None:
            cleaned["cuit"] = re.sub(r"\D", "", str(cuit))

        for field in ("razon_social", "calle", "codigo_postal", "ciudad"):
            if field in cleaned and cleaned[field] is not None:
                cleaned[field] = str(cleaned[field]).strip()

        numero = cleaned.get("numero")
        if numero is not None and numero != "":
            try:
                cleaned["numero"] = int(str(numero).replace(",", "."))
            except (TypeError, ValueError):
                cleaned["numero"] = numero

        for field in ("interes_por_mora", "redondeo_aumento"):
            value = cleaned.get(field)
            if value is not None and value != "":
                try:
                    cleaned[field] = Decimal(str(value).replace(",", "."))
                except (TypeError, ValueError):
                    cleaned[field] = value

        return cleaned

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
            datos_limpios = ConsorcioService._normalize_payload(datos)
            consorcio = Consorcio(**datos_limpios)
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
            datos_limpios = ConsorcioService._normalize_payload(datos)
            for key, value in datos_limpios.items():
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
