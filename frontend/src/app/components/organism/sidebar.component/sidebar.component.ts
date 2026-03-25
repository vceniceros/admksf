import { Component, Input, OnInit } from '@angular/core';
import { ActivatedRoute, Router, NavigationEnd } from '@angular/router';
import { filter } from 'rxjs/operators';
import { NavbarItemComponent } from '../../molecules/navbar-item.component/navbar-item.component';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css'],
  standalone: true,
  imports: [NavbarItemComponent, CommonModule]
})
export class SidebarComponent implements OnInit {
  @Input() isVisible: boolean = false;
  consortiumName: string = '';
  
  dashboardRoute: string = '';
  ownersRoute: string = '';
  unitsRoute: string = '';
  providersRoute: string = '';
  paymentsRoute: string = '';
  monthlyBalanceRoute: string = '';
  expensesRoute: string = '';
  settlementRoute: string = '';

  constructor(
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit() {
    // Obtener consortiumName de la ruta actual
    this.router.events
      .pipe(filter(event => event instanceof NavigationEnd))
      .subscribe(() => {
        this.updateRoutes();
      });
    
    // Verificar ruta inicial
    this.updateRoutes();
  }

  updateRoutes() {
    const url = this.router.url;
    // Extraer el nombre del consorcio de la URL
    const match = url.match(/dashboard\/([^\/]+)/);
    if (match && match[1]) {
      this.consortiumName = match[1];
      this.dashboardRoute = `/dashboard/${this.consortiumName}`;
      this.ownersRoute = `/dashboard/${this.consortiumName}/propietarios`; // Ajustar cuando exista la ruta
      this.unitsRoute = `/dashboard/${this.consortiumName}/unidades`;
      this.providersRoute = `/dashboard/${this.consortiumName}/proveedores`;
      this.paymentsRoute = `/dashboard/${this.consortiumName}/pagos`;
      this.monthlyBalanceRoute = `/dashboard/${this.consortiumName}/saldos-mensuales`;
      this.expensesRoute = `/dashboard/${this.consortiumName}/gastos`;
      this.settlementRoute = `/dashboard/${this.consortiumName}/expensas`;
    }
  }
}