export interface ApiEnvelope<T> {
  status: string;
  message: string;
  data: T;
  errors?: Record<string, string[]>;
}

export interface AuthUser {
  id: number;
  correo_electronico: string;
  nombre: string;
  apellido: string;
  rol: string;
  esta_activo: boolean;
}

export interface AuthSession {
  token: string;
  token_type: string;
  expires_in: number;
  refreshed: boolean;
  usuario: AuthUser;
}

export interface LoginPayload {
  usuario: string;
  contrasena: string;
}

export interface RegisterPayload {
  correo_electronico: string;
  contrasena: string;
  nombre: string;
  apellido: string;
  rol: 'superusuario' | 'administrador';
  esta_activo: boolean;
}

export interface RegisterResult {
  id: number;
  correo_electronico: string;
  nombre: string;
  apellido: string;
  esta_activo: boolean;
  fecha_creacion: string;
  rol: string;
}