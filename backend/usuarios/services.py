"""Servicios para la app usuarios."""

from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from django.utils import timezone

from .auth_service import AuthService
from .models import Rol, Usuario


class UsuarioService:
    """Servicio para gestionar el registro de usuarios."""

    @staticmethod
    def _normalize_payload(datos: dict) -> dict:
        """Normaliza y limpia datos de registro."""
        if not isinstance(datos, dict):
            return {}

        cleaned = dict(datos)

        for field in ("correo_electronico", "nombre", "apellido"):
            if field in cleaned and cleaned[field] is not None:
                cleaned[field] = str(cleaned[field]).strip()

        if "correo_electronico" in cleaned and cleaned["correo_electronico"]:
            cleaned["correo_electronico"] = cleaned["correo_electronico"].lower()

        if "esta_activo" in cleaned:
            cleaned["esta_activo"] = bool(cleaned["esta_activo"])

        return cleaned

    @staticmethod
    def _resolver_rol(datos: dict) -> Rol:
        """Resuelve el rol por nombre o id."""
        rol_id = datos.pop("rol_id", None)
        rol_nombre = datos.pop("rol", None)

        if rol_id is not None:
            return Rol.objects.get(pk=rol_id)

        if rol_nombre is not None:
            return Rol.objects.get(nombre=str(rol_nombre).strip().lower())

        raise ValidationError({"rol": ["El rol es obligatorio."]})

    @staticmethod
    def registrar_usuario(datos: dict) -> Usuario:
        """Registra un nuevo usuario del dominio."""
        datos_limpios = UsuarioService._normalize_payload(datos)

        try:
            rol = UsuarioService._resolver_rol(datos_limpios)
        except Rol.DoesNotExist as exc:
            raise ValidationError({"rol": ["El rol indicado no existe."]}) from exc

        usuario = Usuario(
            correo_electronico=datos_limpios.get("correo_electronico"),
            contrasena=AuthService.generate_hashed_password(datos_limpios.get("contrasena")),
            nombre=datos_limpios.get("nombre"),
            apellido=datos_limpios.get("apellido"),
            esta_activo=datos_limpios.get("esta_activo", True),
            rol=rol,
        )

        usuario.full_clean()
        usuario.save()
        return usuario

    @staticmethod
    def autenticar_usuario(usuario: str, contrasena: str) -> Usuario:
        """Autentica un usuario por correo electrónico y contraseña."""

        identificador = str(usuario).strip().lower()

        try:
            usuario_db = Usuario.objects.select_related("rol").get(
                correo_electronico=identificador,
            )
        except Usuario.DoesNotExist as exc:
            raise ValidationError({"usuario": ["Usuario o contraseña inválidos."]}) from exc

        if not usuario_db.esta_activo:
            raise ValidationError({"usuario": ["El usuario se encuentra inactivo."]})

        if not usuario_db.check_password(contrasena):
            raise ValidationError({"usuario": ["Usuario o contraseña inválidos."]})

        usuario_db.ultimo_ingreso = timezone.now()
        usuario_db.save(update_fields=["ultimo_ingreso"])
        return usuario_db

    @staticmethod
    def validar_sesion(token: str) -> tuple[Usuario, str | None]:
        """Valida una sesión JWT y retorna token refrescado si corresponde."""

        payload = AuthService.decode_jwt(token)

        try:
            usuario = Usuario.objects.select_related("rol").get(pk=payload["sub"])
        except Usuario.DoesNotExist as exc:
            raise ValidationError({"usuario": ["El usuario asociado al token no existe."]}) from exc

        if not usuario.esta_activo:
            raise ValidationError({"usuario": ["El usuario se encuentra inactivo."]})

        refreshed_token = None
        if AuthService.should_refresh_token(payload):
            refreshed_token = AuthService.generate_jwt(usuario)

        return usuario, refreshed_token

    @staticmethod
    def verificar_superusuario(usuario: Usuario) -> None:
        """Valida que el usuario autenticado tenga rol superusuario."""

        if usuario.rol.nombre != "superusuario":
            raise PermissionDenied("Se requiere un usuario con rol superusuario.")

    @staticmethod
    def recuperar_contrasena(
        correo_electronico: str,
        nueva_contrasena: str | None = None,
    ) -> tuple[Usuario, str]:
        """Resetea manualmente la contraseña de un usuario."""

        correo_normalizado = str(correo_electronico).strip().lower()

        try:
            usuario = Usuario.objects.select_related("rol").get(
                correo_electronico=correo_normalizado,
            )
        except Usuario.DoesNotExist as exc:
            raise ValidationError({"correo_electronico": ["El usuario indicado no existe."]}) from exc

        password_plano = nueva_contrasena or AuthService.generate_temporary_password()
        usuario.contrasena = AuthService.generate_hashed_password(password_plano)
        usuario.save(update_fields=["contrasena"])
        return usuario, password_plano