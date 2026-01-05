import { Component, Input } from '@angular/core';
import { IconComponent } from '../../atoms/icon.component/icon.component';
import { LabelComponent } from '../../atoms/label.component/label.component';
import { CommonModule } from '@angular/common';
@Component({
  selector: 'app-navbar-item',
  templateUrl: './navbar-item.component.html',
  styleUrls: ['./navbar-item.component.css'],
  standalone: true,
  imports: [IconComponent, LabelComponent, CommonModule]
})
export class NavbarItemComponent {
  @Input() iconHref!: string; // Referencia al ícono en el sprite
  @Input() label!: string; // Texto del ítem en el navbar
  @Input() isActive: boolean = false; // Estado activo/inactivo
  @Input() size: string = '24'; // Tamaño del ícono
  @Input() iconColor: string = '#000000'; // Color del ícono
}