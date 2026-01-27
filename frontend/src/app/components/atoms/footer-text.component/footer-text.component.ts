import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-footer-text',
  imports: [CommonModule],
  templateUrl: './footer-text.component.html',
  styleUrl: './footer-text.component.css',
  standalone: true
})
export class FooterTextComponent {
  @Input() text!: string; // Texto del footer
  @Input() color: string = '#000'; // Color del texto
  @Input() fontSize: string = '14px'; // Tamaño del texto
}
