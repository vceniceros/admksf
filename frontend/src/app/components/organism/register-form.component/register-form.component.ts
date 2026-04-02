import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Output, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { catchError, finalize, throwError } from 'rxjs';
import { RegisterPayload, RegisterResult } from '../../../../models/auth.model';
import { AuthService } from '../../../services/auth.service';
import { AuthActionButtonComponent } from '../../atoms/auth-action-button.component/auth-action-button.component';
import { AuthFeedbackCardComponent } from '../../molecules/auth-feedback-card.component/auth-feedback-card.component';
import { AuthFieldComponent } from '../../molecules/auth-field.component/auth-field.component';

@Component({
  selector: 'app-register-form',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    AuthActionButtonComponent,
    AuthFieldComponent,
    AuthFeedbackCardComponent
  ],
  templateUrl: './register-form.component.html',
  styleUrl: './register-form.component.css'
})
export class RegisterFormComponent {
  private readonly fb = inject(FormBuilder);
  private readonly authService = inject(AuthService);

  @Output() registrationCompleted = new EventEmitter<string>();
  @Output() switchMode = new EventEmitter<void>();

  readonly form = this.fb.group({
    nombre: ['', [Validators.required, Validators.minLength(2)]],
    apellido: ['', [Validators.required, Validators.minLength(2)]],
    correo_electronico: ['', [Validators.required, Validators.email]],
    contrasena: ['', [Validators.required, Validators.minLength(8)]],
    confirmarContrasena: ['', [Validators.required, Validators.minLength(8)]]
  });

  isSubmitting = false;
  submitError = '';

  submit(): void {
    if (this.form.invalid || this.passwordsDoNotMatch()) {
      this.form.markAllAsTouched();
      return;
    }

    this.isSubmitting = true;
    this.submitError = '';

    const formValue = this.form.getRawValue();
    const payload: RegisterPayload = {
      nombre: formValue.nombre ?? '',
      apellido: formValue.apellido ?? '',
      correo_electronico: formValue.correo_electronico ?? '',
      contrasena: formValue.contrasena ?? '',
      rol: 'administrador',
      esta_activo: true
    };

    this.authService
      .register(payload)
      .pipe(
        catchError((error: unknown) => {
          this.submitError = error instanceof Error ? error.message : 'No se pudo registrar el usuario.';
          return throwError(() => error);
        }),
        finalize(() => {
          this.isSubmitting = false;
        })
      )
      .subscribe({
        next: (result: RegisterResult) => {
          this.form.reset();
          this.registrationCompleted.emit(result.correo_electronico);
        },
        error: () => undefined
      });
  }

  updateField(
    controlName: 'nombre' | 'apellido' | 'correo_electronico' | 'contrasena' | 'confirmarContrasena',
    value: string
  ): void {
    this.form.controls[controlName].setValue(value);
  }

  touchField(
    controlName: 'nombre' | 'apellido' | 'correo_electronico' | 'contrasena' | 'confirmarContrasena'
  ): void {
    this.form.controls[controlName].markAsTouched();
  }

  getError(
    controlName: 'nombre' | 'apellido' | 'correo_electronico' | 'contrasena' | 'confirmarContrasena'
  ): string {
    const control = this.form.controls[controlName];

    if (!control.touched || !control.errors) {
      if (controlName === 'confirmarContrasena' && control.touched && this.passwordsDoNotMatch()) {
        return 'Las contraseñas no coinciden.';
      }
      return '';
    }

    if (control.errors['required']) {
      return 'Este campo es obligatorio.';
    }

    if (control.errors['email']) {
      return 'Ingresá un correo electrónico válido.';
    }

    if (control.errors['minlength']) {
      return 'Este campo no tiene el largo mínimo requerido.';
    }

    if (controlName === 'confirmarContrasena' && this.passwordsDoNotMatch()) {
      return 'Las contraseñas no coinciden.';
    }

    return 'Revisá este campo.';
  }

  private passwordsDoNotMatch(): boolean {
    const { contrasena, confirmarContrasena } = this.form.getRawValue();
    return Boolean(contrasena && confirmarContrasena && contrasena !== confirmarContrasena);
  }
}