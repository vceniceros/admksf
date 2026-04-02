import { Component, EventEmitter, Output, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';


import { IconComponent } from '../../atoms/icon.component/icon.component';
import { AuthService } from '../../../services/auth.service';


@Component({
  selector: 'app-navbar',
  templateUrl: './navbar-component.html',
  styleUrls: ['./navbar-component.css'],
  standalone: true,
  imports: [CommonModule, IconComponent],
})
export class NavbarComponent {
  @Input() showMenuButton: boolean = true; // Controla si se muestra el botón del menú
  @Output() toggleMenu = new EventEmitter<void>(); 

  constructor(
    public authService: AuthService,
    private router: Router
  ) {}

  onMenuClick() {
    this.toggleMenu.emit(); 
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/']);
  }
}
