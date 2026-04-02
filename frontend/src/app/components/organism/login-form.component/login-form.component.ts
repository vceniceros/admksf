import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Output, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { catchError, finalize, throwError } from 'rxjs';
import { LoginPayload } from '../../../../models/auth.model';
import { AuthService } from '../../../services/auth.service';
import { AuthActionButtonComponent } from '../../atoms/auth-action-button.component/auth-action-button.component';
import { AuthFeedbackCardComponent } from '../../molecules/auth-feedback-card.component/auth-feedback-card.component';
import { AuthFieldComponent } from '../../molecules/auth-field.component/auth-field.component';

@Component({
  selector: 'app-login-form',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    AuthActionButtonComponent,
    AuthFieldComponent,
    AuthFeedbackCardComponent
  ],
  templateUrl: './login-form.component.html',
  styleUrl: './login-form.component.css'
})
export class LoginFormComponent {
  private readonly fb = inject(FormBuilder);
  private readonly authService = inject(AuthService);
  private readonly router = inject(Router);

  @Output() switchMode = new EventEmitter<void>();

  readonly form = this.fb.group({
    usuario: ['', [Validators.required, Validators.email]],
    contrasena: ['', [Validators.required, Validators.minLength(8)]]
  });

  isSubmitting = false;
  submitError = '';

  submit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.isSubmitting = true;
    this.submitError = '';

    const payload = this.form.getRawValue() as LoginPayload;

    this.authService
      .login(payload)
      .pipe(
        catchError(error => {
          this.submitError = error instanceof Error ? error.message : 'No se pudo iniciar sesión.';
          return throwError(() => error);
        }),
        finalize(() => {
          this.isSubmitting = false;
        })
      )
      .subscribe({
        next: () => {
          this.router.navigate(['/consorcios']);
        },
        error: () => undefined
      });
  }

  updateField(controlName: 'usuario' | 'contrasena', value: string): void {
    this.form.controls[controlName].setValue(value);
  }

  touchField(controlName: 'usuario' | 'contrasena'): void {
    this.form.controls[controlName].markAsTouched();
  }

  getError(controlName: 'usuario' | 'contrasena'): string {
    const control = this.form.controls[controlName];

    if (!control.touched || !control.errors) {
      return '';
    }

    if (control.errors['required']) {
      return 'Este campo es obligatorio.';
    }

    if (control.errors['email']) {
      return 'Ingresá un correo electrónico válido.';
    }

    if (control.errors['minlength']) {
      return 'La contraseña debe tener al menos 8 caracteres.';
    }

    return 'Revisá este campo.';
  }
}