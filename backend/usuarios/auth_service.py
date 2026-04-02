"""Servicios de autenticación para la app usuarios."""

import os
from datetime import timedelta
from secrets import token_hex
import string
import secrets

import jwt
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.utils import timezone


class AuthService:
    """Encapsula operaciones de hashing de credenciales."""

    SALT_BYTES = 16
    JWT_EXPIRATION_ENV = "JWT_EXPIRATION_SECONDS"
    JWT_REFRESH_WINDOW_ENV = "JWT_REFRESH_WINDOW_SECONDS"
    JWT_SECRET_ENV = "JWT_SECRET_KEY"
    JWT_ALGORITHM_ENV = "JWT_ALGORITHM"
    TEMP_PASSWORD_LENGTH = 16

    @staticmethod
    def generate_hashed_password(raw_password: str) -> str:
        """Genera un hash de Django con una sal aleatoria de 16 bytes."""

        salt = token_hex(AuthService.SALT_BYTES)
        return make_password(raw_password, salt=salt)

    @staticmethod
    def generate_temporary_password(length: int | None = None) -> str:
        """Genera una contraseña temporal segura para recuperación manual."""

        password_length = length or AuthService.TEMP_PASSWORD_LENGTH
        alphabet = string.ascii_letters + string.digits
        return "".join(secrets.choice(alphabet) for _ in range(password_length))

    @staticmethod
    def _get_jwt_secret() -> str:
        """Obtiene el secreto de firmado para JWT."""

        return os.getenv(AuthService.JWT_SECRET_ENV, settings.SECRET_KEY)

    @staticmethod
    def _get_jwt_algorithm() -> str:
        """Obtiene el algoritmo de firmado para JWT."""

        return os.getenv(AuthService.JWT_ALGORITHM_ENV, "HS256")

    @staticmethod
    def get_jwt_expiration_seconds() -> int:
        """Obtiene el tiempo de expiración del JWT en segundos."""

        return int(os.getenv(AuthService.JWT_EXPIRATION_ENV, "1800"))

    @staticmethod
    def get_jwt_refresh_window_seconds() -> int:
        """Obtiene la ventana de refresh automático del JWT en segundos."""

        return int(os.getenv(AuthService.JWT_REFRESH_WINDOW_ENV, "300"))

    @staticmethod
    def generate_jwt(usuario) -> str:
        """Genera un JWT para el usuario autenticado."""

        now = timezone.now()
        expires_at = now + timedelta(seconds=AuthService.get_jwt_expiration_seconds())
        payload = {
            "sub": str(usuario.id),
            "correo_electronico": usuario.correo_electronico,
            "rol": usuario.rol.nombre,
            "esta_activo": usuario.esta_activo,
            "jti": token_hex(8),
            "iat": int(now.timestamp()),
            "exp": int(expires_at.timestamp()),
        }
        return jwt.encode(
            payload,
            AuthService._get_jwt_secret(),
            algorithm=AuthService._get_jwt_algorithm(),
        )

    @staticmethod
    def decode_jwt(token: str) -> dict:
        """Decodifica y valida un JWT."""

        try:
            return jwt.decode(
                token,
                AuthService._get_jwt_secret(),
                algorithms=[AuthService._get_jwt_algorithm()],
            )
        except jwt.ExpiredSignatureError as exc:
            raise ValidationError({"token": ["El token expiró."]}) from exc
        except jwt.InvalidTokenError as exc:
            raise ValidationError({"token": ["El token es inválido."]}) from exc

    @staticmethod
    def extract_bearer_token(authorization_header: str | None) -> str:
        """Extrae el token Bearer desde el header Authorization."""

        if not authorization_header:
            raise ValidationError({"authorization": ["Header Authorization requerido."]})

        prefix = "Bearer "
        if not authorization_header.startswith(prefix):
            raise ValidationError({"authorization": ["Formato Authorization inválido."]})

        return authorization_header[len(prefix):].strip()

    @staticmethod
    def should_refresh_token(payload: dict) -> bool:
        """Indica si el token debe refrescarse por proximidad al vencimiento."""

        remaining_seconds = int(payload["exp"] - timezone.now().timestamp())
        return remaining_seconds <= AuthService.get_jwt_refresh_window_seconds()

    @staticmethod
    def build_auth_response(usuario, token: str, refreshed: bool = False) -> dict:
        """Arma la respuesta estándar de autenticación."""

        return {
            "token": token,
            "token_type": "Bearer",
            "expires_in": AuthService.get_jwt_expiration_seconds(),
            "refreshed": refreshed,
            "usuario": {
                "id": usuario.id,
                "correo_electronico": usuario.correo_electronico,
                "nombre": usuario.nombre,
                "apellido": usuario.apellido,
                "rol": usuario.rol.nombre,
                "esta_activo": usuario.esta_activo,
            },
        }