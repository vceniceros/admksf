import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable, computed, inject, signal } from '@angular/core';
import { Observable, catchError, map, of, tap, throwError } from 'rxjs';
import {
  ApiEnvelope,
  AuthSession,
  AuthUser,
  LoginPayload,
  RegisterPayload,
  RegisterResult
} from '../../models/auth.model';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly sessionStorageKey = 'consorcio360.auth.session';
  private readonly loginUrl = '/api/usuarios/login/';
  private readonly registerUrl = '/api/usuarios/registrar/';
  private readonly verifyUrl = '/api/usuarios/autenticado/';
  private readonly sessionState = signal<AuthSession | null>(this.readStoredSession());

  readonly session = computed(() => this.sessionState());
  readonly user = computed<AuthUser | null>(() => this.sessionState()?.usuario ?? null);
  readonly isAuthenticated = computed(() => Boolean(this.sessionState()?.token));

  login(payload: LoginPayload): Observable<AuthSession> {
    return this.http.post<ApiEnvelope<AuthSession>>(this.loginUrl, payload).pipe(
      map(response => response.data),
      tap(session => this.setSession(session)),
      catchError(this.handleHttpError<AuthSession>('No se pudo iniciar sesión.'))
    );
  }

  register(payload: RegisterPayload): Observable<RegisterResult> {
    return this.http.post<ApiEnvelope<RegisterResult>>(this.registerUrl, payload).pipe(
      map(response => response.data),
      catchError(this.handleHttpError<RegisterResult>('No se pudo registrar el usuario.'))
    );
  }

  verifySession(): Observable<AuthSession> {
    return this.http.get<ApiEnvelope<AuthSession>>(this.verifyUrl).pipe(
      map(response => response.data),
      tap(session => this.setSession(session)),
      catchError(this.handleHttpError<AuthSession>('La sesión ya no es válida.'))
    );
  }

  bootstrapSession(): Observable<AuthSession | null> {
    if (!this.getToken()) {
      return of(null);
    }

    return this.verifySession().pipe(
      map(session => session),
      catchError(() => {
        this.clearSession();
        return of(null);
      })
    );
  }

  ensureAuthenticated(): Observable<boolean> {
    if (!this.getToken()) {
      return of(false);
    }

    return this.verifySession().pipe(
      map(() => true),
      catchError(() => {
        this.clearSession();
        return of(false);
      })
    );
  }

  logout(): void {
    this.clearSession();
  }

  clearSession(): void {
    this.sessionState.set(null);
    if (this.isBrowser()) {
      window.localStorage.removeItem(this.sessionStorageKey);
    }
  }

  getToken(): string | null {
    return this.sessionState()?.token ?? null;
  }

  extractErrorMessage(error: unknown, fallback = 'Ocurrió un error inesperado.'): string {
    if (!(error instanceof HttpErrorResponse)) {
      return fallback;
    }

    const backendMessage = error.error?.message;
    const backendErrors = error.error?.errors as Record<string, string[]> | undefined;

    if (backendErrors) {
      const firstError = Object.values(backendErrors)
        .flat()
        .find(Boolean);

      if (firstError) {
        return firstError;
      }
    }

    if (typeof backendMessage === 'string' && backendMessage.trim()) {
      return backendMessage;
    }

    return fallback;
  }

  handleHttpError<T>(fallback: string) {
    return (error: unknown): Observable<T> => {
      const message = this.extractErrorMessage(error, fallback);
      return throwError(() => new Error(message));
    };
  }

  private setSession(session: AuthSession): void {
    this.sessionState.set(session);

    if (this.isBrowser()) {
      window.localStorage.setItem(this.sessionStorageKey, JSON.stringify(session));
    }
  }

  private readStoredSession(): AuthSession | null {
    if (!this.isBrowser()) {
      return null;
    }

    const rawSession = window.localStorage.getItem(this.sessionStorageKey);
    if (!rawSession) {
      return null;
    }

    try {
      return JSON.parse(rawSession) as AuthSession;
    } catch {
      window.localStorage.removeItem(this.sessionStorageKey);
      return null;
    }
  }

  private isBrowser(): boolean {
    return typeof window !== 'undefined' && typeof window.localStorage !== 'undefined';
  }
}