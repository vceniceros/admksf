import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { AuthInputComponent } from '../../atoms/auth-input.component/auth-input.component';

@Component({
  selector: 'app-auth-field',
  standalone: true,
  imports: [CommonModule, AuthInputComponent],
  templateUrl: './auth-field.component.html',
  styleUrl: './auth-field.component.css'
})
export class AuthFieldComponent {
  @Input() label = '';
  @Input() type = 'text';
  @Input() placeholder = '';
  @Input() value = '';
  @Input() error = '';
  @Input() autocomplete = 'off';
  @Input() inputMode: 'text' | 'email' | 'numeric' | 'decimal' | 'search' | 'tel' | 'url' = 'text';
  @Input() disabled = false;
  @Input() helpText = '';

  @Output() valueChange = new EventEmitter<string>();
  @Output() blurInput = new EventEmitter<void>();
}