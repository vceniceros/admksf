import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-auth-input',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './auth-input.component.html',
  styleUrl: './auth-input.component.css'
})
export class AuthInputComponent {
  @Input() type = 'text';
  @Input() placeholder = '';
  @Input() value = '';
  @Input() autocomplete = 'off';
  @Input() inputMode: 'text' | 'email' | 'numeric' | 'decimal' | 'search' | 'tel' | 'url' = 'text';
  @Input() disabled = false;

  @Output() valueChange = new EventEmitter<string>();
  @Output() blurInput = new EventEmitter<void>();

  onInput(event: Event): void {
    const target = event.target as HTMLInputElement;
    this.valueChange.emit(target.value);
  }

  onBlur(): void {
    this.blurInput.emit();
  }
}