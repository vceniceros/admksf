"""Modelos de usuarios y roles del dominio.

Fecha:
    01 - 04 - 2026
"""

from django.contrib.auth.hashers import check_password
from django.core.validators import EmailValidator
from django.db import models
from django.utils import timezone

from shared import build_model_str

from .auth_service import AuthService


class Rol(models.Model):
    """Representa un rol funcional del sistema."""

    nombre = models.CharField(max_length=50, unique=True, db_column="nombre")

    class Meta:
        db_table = "roles"
        verbose_name = "Rol"
        verbose_name_plural = "Roles"
        ordering = ["nombre"]

    def __str__(self) -> str:
        """Devuelve una representación legible del rol."""

        return build_model_str(
            "Rol",
            [("nombre", self.nombre, False)],
        )


class Usuario(models.Model):
    """Representa un usuario administrativo del dominio."""

    correo_electronico = models.EmailField(
        max_length=254,
        unique=True,
        db_column="correo_electronico",
        validators=[EmailValidator()],
    )
    contrasena = models.CharField(max_length=128, db_column="contrasena")
    fecha_creacion = models.DateTimeField(
        default=timezone.now,
        db_column="fecha_creacion",
        editable=False,
    )
    ultimo_ingreso = models.DateTimeField(
        null=True,
        blank=True,
        db_column="ultimo_ingreso",
    )
    esta_activo = models.BooleanField(default=True, db_column="esta_activo")
    nombre = models.CharField(max_length=100, db_column="nombre")
    apellido = models.CharField(max_length=100, db_column="apellido")
    rol = models.ForeignKey(
        Rol,
        on_delete=models.PROTECT,
        related_name="usuarios",
        db_column="rol_id",
    )

    class Meta:
        db_table = "usuarios"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ["apellido", "nombre", "correo_electronico"]

    def __str__(self) -> str:
        """Devuelve una representación legible del usuario."""

        return build_model_str(
            "Usuario",
            [
                ("correo_electronico", self.correo_electronico, False),
                ("nombre", self.nombre, False),
                ("apellido", self.apellido, False),
                ("fecha_creacion", self.fecha_creacion, True),
                ("esta_activo", self.esta_activo, False),
                ("rol", self.rol_id, True),
            ],
        )

    def set_password(self, raw_password: str) -> None:
        """Guarda la contraseña usando el hasher configurado por Django."""

        self.contrasena = AuthService.generate_hashed_password(raw_password)

    def check_password(self, raw_password: str) -> bool:
        """Valida una contraseña contra el hash almacenado."""

        return check_password(raw_password, self.contrasena)

    def save(self, *args, **kwargs):
        """Evita persistir contraseñas en texto plano."""

        if self.contrasena and not self.contrasena.startswith(("pbkdf2_", "argon2$", "bcrypt$", "scrypt$")):
            self.contrasena = AuthService.generate_hashed_password(self.contrasena)
        super().save(*args, **kwargs)