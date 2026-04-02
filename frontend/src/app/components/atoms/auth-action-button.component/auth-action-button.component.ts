import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-auth-action-button',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './auth-action-button.component.html',
  styleUrl: './auth-action-button.component.css'
})
export class AuthActionButtonComponent {
  @Input() label = 'Continuar';
  @Input() disabled = false;
  @Input() loading = false;
}