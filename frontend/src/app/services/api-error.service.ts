import { HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';

export interface ApiErrorShape {
  message?: string;
  errors?: Record<string, string[] | string>;
}

export class AppHttpError extends Error {
  constructor(
    message: string,
    readonly status: number,
    readonly errors?: Record<string, string[] | string>
  ) {
    super(message);
    this.name = 'AppHttpError';
  }
}

@Injectable({
  providedIn: 'root'
})
export class ApiErrorService {
  extractMessage(error: unknown, fallback = 'Ocurrió un error inesperado.'): string {
    if (!(error instanceof HttpErrorResponse)) {
      if (error instanceof Error && error.message.trim()) {
        return error.message;
      }
      return fallback;
    }

    const payload = this.getPayload(error);
    const fieldErrors = payload?.errors;

    if (fieldErrors) {
      const firstError = Object.values(fieldErrors)
        .flatMap(value => (Array.isArray(value) ? value : [value]))
        .find(value => typeof value === 'string' && value.trim());

      if (firstError) {
        return firstError;
      }
    }

    if (typeof payload?.message === 'string' && payload.message.trim()) {
      return payload.message;
    }

    if (typeof error.message === 'string' && error.message.trim()) {
      return error.message;
    }

    return fallback;
  }

  extractDetailedMessage(error: unknown, fallback = 'Ocurrió un error inesperado.'): string {
    if (!(error instanceof HttpErrorResponse)) {
      return this.extractMessage(error, fallback);
    }

    const payload = this.getPayload(error);
    const baseMessage = this.extractMessage(error, fallback);
    const fieldErrors = payload?.errors;

    if (!fieldErrors) {
      return baseMessage;
    }

    const details = Object.entries(fieldErrors)
      .map(([field, messages]) => {
        const normalized = Array.isArray(messages) ? messages.join(', ') : String(messages);
        return `${field}: ${normalized}`;
      })
      .join(' | ');

    return details ? `${baseMessage} (${details})` : baseMessage;
  }

  toAppError(error: unknown, fallback = 'Ocurrió un error inesperado.'): AppHttpError {
    if (error instanceof AppHttpError) {
      return error;
    }

    if (error instanceof HttpErrorResponse) {
      const payload = this.getPayload(error);
      return new AppHttpError(this.extractMessage(error, fallback), error.status, payload?.errors);
    }

    if (error instanceof Error) {
      return new AppHttpError(error.message || fallback, 0);
    }

    return new AppHttpError(fallback, 0);
  }

  private getPayload(error: HttpErrorResponse): ApiErrorShape | null {
    if (!error.error || typeof error.error !== 'object') {
      return null;
    }

    return error.error as ApiErrorShape;
  }
}