import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-icon',
  templateUrl: './icon.component.html',
  styleUrls: ['./icon.component.css'],
  standalone: true 
})
export class IconComponent {
  @Input() size: string = '24';  // Tamaño del ícono en pixeles
  @Input() color: string = '#000000';  // Color del ícono en formato hexadecimal
  @Input() iconHref!: string;  // Referencia al ícono SVG como una URL o ruta de archivo
}