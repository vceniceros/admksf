import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
@Component({
  selector: 'app-generic-button',
  templateUrl: './generic-button.component.html',
  styleUrls: ['./generic-button.component.css'],
  imports: [CommonModule],
  standalone: true
})
export class GenericButtonComponent {
  @Input() type: 'success' | 'danger' | 'warning' | 'default' = 'default';
  @Input() label!: string; 
}