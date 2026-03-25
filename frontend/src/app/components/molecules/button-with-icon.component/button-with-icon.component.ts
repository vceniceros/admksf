import { Component, Input } from '@angular/core';
import { IconComponent } from '../../atoms/icon.component/icon.component'; 
import { GenericButtonComponent } from '../../atoms/generic-button.component/generic-button.component';
import { CommonModule } from '@angular/common';
@Component({
  selector: 'app-button-with-icon',
  templateUrl: './button-with-icon.component.html',
  styleUrls: ['./button-with-icon.component.css'],
  standalone: true,
  imports: [IconComponent, GenericButtonComponent, CommonModule] 
})
export class ButtonWithIconComponent {
  @Input() iconHref!: string; // Referencia al ícono en el sprite
  @Input() label!: string; // Texto del botón
  @Input() size: string = '24'; // Tamaño del ícono
  @Input() iconColor: string = '#000000'; // Color del ícono
  @Input() type: 'success' | 'danger' | 'warning' | 'default' = 'default'; // Tipo de botón
}
