import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { AuthMode, AuthModeToggleComponent } from '../../molecules/auth-mode-toggle.component/auth-mode-toggle.component';
import { AuthFeedbackCardComponent } from '../../molecules/auth-feedback-card.component/auth-feedback-card.component';
import { LoginFormComponent } from '../../organism/login-form.component/login-form.component';
import { RegisterFormComponent } from '../../organism/register-form.component/register-form.component';

@Component({
  selector: 'app-auth-access',
  standalone: true,
  imports: [
    CommonModule,
    AuthModeToggleComponent,
    AuthFeedbackCardComponent,
    LoginFormComponent,
    RegisterFormComponent
  ],
  templateUrl: './auth-access.component.html',
  styleUrl: './auth-access.component.css'
})
export class AuthAccessComponent {
  mode: AuthMode = 'login';
  registerSuccessEmail = '';

  setMode(mode: AuthMode): void {
    this.mode = mode;
  }

  handleRegistrationCompleted(correoElectronico: string): void {
    this.registerSuccessEmail = correoElectronico;
    this.mode = 'login';
  }
}