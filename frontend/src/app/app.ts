import { Component, signal, OnInit, HostListener } from '@angular/core';
import { RouterOutlet, Router, NavigationEnd } from '@angular/router';
import { filter } from 'rxjs/operators';
import { IconComponent } from './components/atoms/icon.component/icon.component';
import { GenericButtonComponent } from './components/atoms/generic-button.component/generic-button.component';
import { ButtonWithIconComponent } from './components/molecules/button-with-icon.component/button-with-icon.component';
import { LabelComponent } from './components/atoms/label.component/label.component';
import { CommonModule } from '@angular/common';
import { NavbarItemComponent } from './components/molecules/navbar-item.component/navbar-item.component';
import { NavbarComponent } from './components/organism/navbar-component/navbar-component';
import { SidebarComponent } from './components/organism/sidebar.component/sidebar.component';
import { FooterComponent } from './components/organism/footer.component/footer.component';

@Component({
  selector: 'app-root',
  template: `
    <div class="flex flex-col h-screen">
      <app-navbar [showMenuButton]="showSidebar" (toggleMenu)="toggleSidebar()"></app-navbar>

      <div class="flex flex-1 overflow-hidden relative">
        <app-sidebar *ngIf="showSidebar" [isVisible]="isSidebarOpen"></app-sidebar>

        <main [class]="showSidebar ? 'flex-1 overflow-auto p-4 bg-gray-50' : 'flex-1 overflow-auto bg-gray-50 main-no-sidebar'">
           <router-outlet></router-outlet>
        </main>
      </div>
      <app-footer></app-footer>
    </div>
  `,
  styleUrl: './app.css',
  imports: [RouterOutlet, IconComponent, GenericButtonComponent, ButtonWithIconComponent, LabelComponent, CommonModule, NavbarItemComponent, NavbarComponent, SidebarComponent, FooterComponent],
  standalone: true
})
export class App implements OnInit {
  protected readonly title = signal('frontend');
  isSidebarOpen = false;
  showSidebar = false; // Controla si se muestra el sidebar (no en la página de selección)

  constructor(private router: Router) {}

  ngOnInit() {
    // Detectar cambios de ruta
    this.router.events
      .pipe(filter(event => event instanceof NavigationEnd))
      .subscribe((event: NavigationEnd) => {
        this.updateSidebarVisibility(event.urlAfterRedirects);
      });

    // Verificar ruta inicial
    if (typeof window !== 'undefined') {
      this.updateSidebarVisibility(this.router.url);
    }

    // Detectar si estamos en desktop al cargar (solo si sidebar debe mostrarse)
    this.checkScreenSize();
  }

  updateSidebarVisibility(url: string) {
    // El sidebar solo se muestra si NO estamos en la ruta raíz (selección de consorcio)
    this.showSidebar = url !== '/';
    
    if (this.showSidebar) {
      this.checkScreenSize();
    } else {
      this.isSidebarOpen = false;
    }
  }

  @HostListener('window:resize')
  onResize() {
    if (this.showSidebar) {
      this.checkScreenSize();
    }
  }

  checkScreenSize() {
    // Verificar que estamos en el navegador (no en el servidor)
    if (typeof window !== 'undefined') {
      // En desktop (768px o más), siempre visible
      if (window.innerWidth >= 768 && this.showSidebar) {
        this.isSidebarOpen = true;
      }
    }
  }

  toggleSidebar() {
    // Solo permite toggle si el sidebar está habilitado
    if (this.showSidebar) {
      this.isSidebarOpen = !this.isSidebarOpen;
    }
  }

}
