import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { DashboardService } from '../../../services/dashboard.service';
import { ServicesService } from '../../../services/services.service';
import { PaymentService } from '../../../services/payment.services';
import { NotificationsService } from '../../../services/notifications.service';
import { ConsortiumService } from '../../../services/consortium.service';
import { DashboardSummary } from '../../../../models/dashboardSummary.model';
import { ServiceStatusItem } from '../../../../models/services.model';
import { Payment } from '../../../../models/payment.model';
import { Notification } from '../../../../models/notifications.model';
import { Consortium } from '../../../../models/consortium.model';
import { Event } from '../../../../models/event.model';
import { ConsortiumDashboardCardsComponent } from '../../molecules/consortium-dashboard-cards.component/consortium-dashboard-cards.component';
import { ConsortiumServicesStatusCardComponent } from '../../molecules/consortium-services-status-card.component/consortium-services-status-card.component';
import { ConsortiumLastPaymentCardFoundCardComponent } from '../../molecules/consortium-last-payment-card-found-card.component/consortium-last-payment-card-found-card.component';
import { ConsortiumCollectionRatesCardComponent } from '../../molecules/consortium-collection-rates-card.component/consortium-collection-rates-card.component';
import { ConsortiumOcupationRateCardComponent } from '../../molecules/consortium-ocupation-rate-card.component/consortium-ocupation-rate-card.component';
import { ConsortiumEventsCardComponent } from '../../molecules/consortium-events-card.component/consortium-events-card.component';
import { LabelComponent } from '../../atoms/label.component/label.component';
import { IconComponent } from '../../atoms/icon.component/icon.component';

@Component({
  selector: 'app-dashboard',
  imports: [
    CommonModule,
    RouterModule,
    ConsortiumDashboardCardsComponent,
    ConsortiumServicesStatusCardComponent,
    ConsortiumLastPaymentCardFoundCardComponent,
    ConsortiumCollectionRatesCardComponent,
    ConsortiumOcupationRateCardComponent,
    ConsortiumEventsCardComponent,
    LabelComponent,
    IconComponent
  ],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css',
  standalone: true
})
export class Dashboard implements OnInit {
  consortiumName: string = '';
  consortiumId: string = "";
  dashboardSummary: DashboardSummary | null = null;
  servicesStatus: ServiceStatusItem[] = [];
  lastPayments: Payment[] = [];
  notifications: Notification[] = [];
  events: Event[] = [];
  consortium: Consortium | null = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private http: HttpClient,
    private dashboardService: DashboardService,
    private servicesService: ServicesService,
    private paymentService: PaymentService,
    private notificationsService: NotificationsService,
    private consortiumService: ConsortiumService
  ) {}

  ngOnInit() {
    this.route.params.subscribe(params => {
      const consortiumNameParam = params['consortiumName'];
      if (consortiumNameParam) {
        this.consortiumName = decodeURIComponent(consortiumNameParam.replace(/-/g, ' '));
        this.loadConsortiumData();
      } else {
        // Si no hay parámetro, redirigir al primer consorcio activo
        this.consortiumService.getAllConsortiums().subscribe({
          next: (consortia) => {
            const firstActive = consortia.find(c => c.status === 'ACTIVE');
            if (firstActive) {
              const nameForUrl = firstActive.name.toLowerCase().replace(/\s+/g, '-');
              this.router.navigate(['/dashboard', nameForUrl]);
            }
          }
        });
      }
    });
  }

  loadConsortiumData() {
    // Cargar consorcio por nombre
    this.consortiumService.getAllConsortiums().subscribe({
      next: (consortia) => {
        const found = consortia.find(c => 
          c.name.toLowerCase() === this.consortiumName.toLowerCase()
        );
        if (found && found.status === 'ACTIVE') {
          this.consortium = found;
          this.consortiumId = found.id;
          this.loadDashboardData();
        } else {
          // Si no se encuentra o no está activo, redirigir al primero activo
          const firstActive = consortia.find(c => c.status === 'ACTIVE');
          if (firstActive) {
            const nameForUrl = firstActive.name.toLowerCase().replace(/\s+/g, '-');
            this.router.navigate(['/dashboard', nameForUrl], { replaceUrl: true });
          } else {
            // Si no hay consorcios activos, redirigir al menú
            this.router.navigate(['/'], { replaceUrl: true });
          }
        }
      },
      error: () => {
        this.router.navigate(['/'], { replaceUrl: true });
      }
    });
  }

  loadDashboardData() {
    // Cargar dashboard summary
    this.dashboardService.getDashboardSummary(this.consortiumId).subscribe({
      next: (data) => this.dashboardSummary = data
    });

    // Cargar servicios
    this.servicesService.getServicesStatus(this.consortiumId).subscribe({
      next: (data) => this.servicesStatus = data
    });

    // Cargar pagos
    this.paymentService.getLastPayments(this.consortiumId).subscribe({
      next: (data) => this.lastPayments = data
    });

    // Cargar notificaciones
    this.notificationsService.getNotifications(this.consortiumId).subscribe({
      next: (data) => this.notifications = data
    });

    // Cargar eventos
    this.http.get<{ status: string; data: any[] }>(`/api/caratulas/consorcio/${this.consortiumId}/`).subscribe({
      next: (response) => {
        const data = response?.data || [];
        this.events = data.map((item, index) => ({
          id: index + 1,
          date: this.formatDate(item.fecha),
          description: item.texto ?? item.texto_preview ?? ''
        }));
      },
      error: () => {
        this.events = [];
      }
    });
  }

  private formatDate(value: string): string {
    if (!value) {
      return '';
    }
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) {
      return value;
    }
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    return `${day}/${month}/${year}`;
  }
}
