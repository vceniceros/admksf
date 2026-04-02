import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';

export type AuthMode = 'login' | 'register';

@Component({
  selector: 'app-auth-mode-toggle',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './auth-mode-toggle.component.html',
  styleUrl: './auth-mode-toggle.component.css'
})
export class AuthModeToggleComponent {
  @Input() mode: AuthMode = 'login';
  @Output() modeChange = new EventEmitter<AuthMode>();
}