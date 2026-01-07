import { Component, EventEmitter, Output, Input } from '@angular/core';
import { CommonModule } from '@angular/common';


import { IconComponent } from '../../atoms/icon.component/icon.component';
import { LabelComponent } from '../../atoms/label.component/label.component';
import { ButtonWithIconComponent } from '../../molecules/button-with-icon.component/button-with-icon.component';


@Component({
  selector: 'app-navbar',
  templateUrl: './navbar-component.html',
  styleUrls: ['./navbar-component.css'],
  standalone: true,
  imports: [CommonModule, IconComponent, LabelComponent, ButtonWithIconComponent],
})
export class NavbarComponent {
  @Input() showMenuButton: boolean = true; // Controla si se muestra el botón del menú
  @Output() toggleMenu = new EventEmitter<void>(); 

  onMenuClick() {
    this.toggleMenu.emit(); 
  }
}
