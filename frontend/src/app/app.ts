import { Component, signal, OnInit, HostListener } from '@angular/core';
import { RouterOutlet, Router, NavigationEnd, NavigationStart, NavigationCancel, NavigationError } from '@angular/router';
import { filter } from 'rxjs/operators';
import { take } from 'rxjs';
import { CommonModule } from '@angular/common';
import { NavbarComponent } from './components/organism/navbar-component/navbar-component';
import { SidebarComponent } from './components/organism/sidebar.component/sidebar.component';
import { FooterComponent } from './components/organism/footer.component/footer.component';
import { AuthService } from './services/auth.service';

@Component({
  selector: 'app-root',
  template: `
    <div class="flex flex-col h-screen">
      <app-navbar [showMenuButton]="showSidebar" (toggleMenu)="toggleSidebar()"></app-navbar>

      <div class="flex flex-1 overflow-hidden relative content-container">
        <app-sidebar *ngIf="showSidebar" [isVisible]="isSidebarOpen || isDesktop()"></app-sidebar>

        <main [class]="showSidebar ? 'main-with-sidebar' : 'main-no-sidebar'">
           <router-outlet></router-outlet>
        </main>

        <div class="loading-overlay" *ngIf="isLoading">
          <div class="loading-content">
            <div class="spinner" aria-label="Cargando" role="status"></div>
            <span class="loading-text">Cargando...</span>
          </div>
        </div>
      </div>
      <app-footer></app-footer>
    </div>
  `,
  styleUrl: './app.css',
  imports: [RouterOutlet, CommonModule, NavbarComponent, SidebarComponent, FooterComponent],
  standalone: true
})
export class App implements OnInit {
  protected readonly title = signal('frontend');
  isSidebarOpen = false;
  showSidebar = false; // Controla si se muestra el sidebar (no en la página de selección)
  isLoading = true;
  private pendingNavigation = 0;

  constructor(
    private router: Router,
    private authService: AuthService
  ) {}

  ngOnInit() {
    this.authService.bootstrapSession().pipe(take(1)).subscribe();

    this.router.events.subscribe(event => {
      if (event instanceof NavigationStart) {
        this.pendingNavigation += 1;
        this.isLoading = true;
      }

      if (event instanceof NavigationEnd || event instanceof NavigationCancel || event instanceof NavigationError) {
        this.pendingNavigation = Math.max(0, this.pendingNavigation - 1);
        if (this.pendingNavigation === 0) {
          this.isLoading = false;
        }
      }
    });

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
    this.showSidebar = url.startsWith('/dashboard/');
    
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

  isDesktop(): boolean {
    if (typeof window !== 'undefined') {
      return window.innerWidth >= 768;
    }
    return false;
  }

  checkScreenSize() {
    // Verificar que estamos en el navegador (no en el servidor)
    if (typeof window !== 'undefined') {
      // En desktop (768px o más), siempre visible y forzado
      if (this.isDesktop() && this.showSidebar) {
        this.isSidebarOpen = true;
      }
      // En mobile, mantener el estado actual (solo cambiar si el usuario interactúa)
    }
  }

  toggleSidebar() {
    // Solo permite toggle si el sidebar está habilitado
    if (this.showSidebar) {
      this.isSidebarOpen = !this.isSidebarOpen;
    }
  }

}
