import { Component, signal, OnInit, HostListener } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { IconComponent } from './components/atoms/icon.component/icon.component';
import { GenericButtonComponent } from './components/atoms/generic-button.component/generic-button.component';
import { ButtonWithIconComponent } from './components/molecules/button-with-icon.component/button-with-icon.component';
import { LabelComponent } from './components/atoms/label.component/label.component';
import { CommonModule } from '@angular/common';
import { NavbarItemComponent } from './components/molecules/navbar-item.component/navbar-item.component';
import { NavbarComponent } from './components/organism/navbar-component/navbar-component';
import { SidebarComponent } from './components/organism/sidebar.component/sidebar.component';

@Component({
  selector: 'app-root',
  template: `
    <div class="flex flex-col h-screen">
      <app-navbar (toggleMenu)="toggleSidebar()"></app-navbar>

      <div class="flex flex-1 overflow-hidden relative">
        <app-sidebar [isVisible]="isSidebarOpen"></app-sidebar>

        <main class="flex-1 overflow-auto p-4 bg-gray-50">
           <router-outlet></router-outlet>
        </main>
      </div>
    </div>
  `,
  styleUrl: './app.css',
  imports: [RouterOutlet, IconComponent, GenericButtonComponent, ButtonWithIconComponent, LabelComponent, CommonModule, NavbarItemComponent, NavbarComponent, SidebarComponent],
  standalone: true
})
export class App implements OnInit {
  protected readonly title = signal('frontend');
  isSidebarOpen = false; // Empieza oculto en mobile

  ngOnInit() {
    // Detectar si estamos en desktop al cargar
    this.checkScreenSize();
  }

  @HostListener('window:resize')
  onResize() {
    this.checkScreenSize();
  }

  checkScreenSize() {
    // En desktop (768px o más), siempre visible
    if (window.innerWidth >= 768) {
      this.isSidebarOpen = true;
    }
    // En mobile, mantener el estado actual (oculto por defecto)
    // No forzar a false aquí para no interrumpir si el usuario lo abrió
  }

  toggleSidebar() {
    this.isSidebarOpen = !this.isSidebarOpen;
  }

}
