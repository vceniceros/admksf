import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-label',
  templateUrl: './label.component.html',
  styleUrls: ['./label.component.css'],
  imports: [CommonModule],
  standalone: true
})
export class LabelComponent {
  @Input() text!: string; // Texto de la etiqueta 
  @Input() color: string = '#000'; // Color del texto
  @Input() fontSize: string = '16px'; // Tamaño del texto
}