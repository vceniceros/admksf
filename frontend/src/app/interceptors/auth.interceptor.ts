import { HttpErrorResponse, HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';
import { AuthService } from '../services/auth.service';
import { ApiErrorService } from '../services/api-error.service';

export const authInterceptor: HttpInterceptorFn = (request, next) => {
  const authService = inject(AuthService);
  const apiErrorService = inject(ApiErrorService);
  const router = inject(Router);
  const token = authService.getToken();
  const isApiCall = request.url.startsWith('/api/');
  const isAuthRequest =
    request.url.startsWith('/api/usuarios/login/') || request.url.startsWith('/api/usuarios/registrar/');

  const authorizedRequest =
    isApiCall && token && !isAuthRequest
      ? request.clone({
          setHeaders: {
            Authorization: `Bearer ${token}`
          }
        })
      : request;

  return next(authorizedRequest).pipe(
    catchError((error: unknown) => {
      if (error instanceof HttpErrorResponse && error.status === 401) {
        authService.clearSession();
        if (!isAuthRequest) {
          void router.navigateByUrl('/');
        }
      }

      return throwError(() => apiErrorService.toAppError(error));
    })
  );
};