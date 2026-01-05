import { Component, signal } from '@angular/core';
import { IconComponent } from './components/atoms/icon.component/icon.component';
import { GenericButtonComponent } from './components/atoms/generic-button.component/generic-button.component';
import { ButtonWithIconComponent } from './components/molecules/button-with-icon.component/button-with-icon.component';
import { LabelComponent } from './components/atoms/label.component/label.component';
import { CommonModule } from '@angular/common';
import { NavbarItemComponent } from './components/molecules/navbar-item.component/navbar-item.component';
@Component({
  selector: 'app-root',
  templateUrl: './app.html',
  styleUrl: './app.css',
  imports: [IconComponent, GenericButtonComponent, ButtonWithIconComponent, LabelComponent, CommonModule, NavbarItemComponent],
})
export class App {
  protected readonly title = signal('frontend');
}
