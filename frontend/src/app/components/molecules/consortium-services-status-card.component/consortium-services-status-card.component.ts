import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ServiceStatusItem } from '../../../../models/services.model';
import { IconComponent } from '../../atoms/icon.component/icon.component';
import { LabelComponent } from '../../atoms/label.component/label.component';

@Component({
  selector: 'app-consortium-services-status-card',
  imports: [CommonModule, IconComponent, LabelComponent],
  templateUrl: './consortium-services-status-card.component.html',
  styleUrl: './consortium-services-status-card.component.css',
  standalone: true
})
export class ConsortiumServicesStatusCardComponent {
  @Input() services!: ServiceStatusItem[];

  getServiceIcon(serviceId: string): string {
    const iconMap: { [key: string]: string } = {
      'water': 'assets/img/sprites.svg#water',
      'electricity': 'assets/img/sprites.svg#lightning',
      'internet': 'assets/img/sprites.svg#wifi',
      'elevator': 'assets/img/sprites.svg#elevator'
    };
    return iconMap[serviceId] || 'assets/img/sprites.svg#building';
  }

  getStatusIcon(status: string): string {
    return status === 'OK' ? 'assets/img/sprites.svg#check' : 'assets/img/sprites.svg#clock';
  }

  getStatusColor(status: string): string {
    return status === 'OK' ? '#10B981' : '#F97316';
  }

  toggleServiceStatus(service: ServiceStatusItem): void {
    service.status = service.status === 'OK' ? 'WARNING' : 'OK';
  }
}
