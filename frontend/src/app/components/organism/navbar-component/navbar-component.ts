import { Component, EventEmitter, Output } from '@angular/core';


import { IconComponent } from '../../atoms/icon.component/icon.component';
import { LabelComponent } from '../../atoms/label.component/label.component';
import { ButtonWithIconComponent } from '../../molecules/button-with-icon.component/button-with-icon.component';


@Component({
  selector: 'app-navbar',
  templateUrl: './navbar-component.html',
  styleUrls: ['./navbar-component.css'],
  standalone: true,
  imports: [IconComponent, LabelComponent, ButtonWithIconComponent],
})
export class NavbarComponent {
 @Output() toggleMenu = new EventEmitter<void>(); 

  onMenuClick() {
    this.toggleMenu.emit(); 
  }
}
