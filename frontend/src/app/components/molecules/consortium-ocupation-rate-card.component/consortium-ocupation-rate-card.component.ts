import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OccupancyMetrics } from '../../../../models/dashboardSummary.model';
import { IconComponent } from '../../atoms/icon.component/icon.component';
import { LabelComponent } from '../../atoms/label.component/label.component';

@Component({
  selector: 'app-consortium-ocupation-rate-card',
  imports: [CommonModule, IconComponent, LabelComponent],
  templateUrl: './consortium-ocupation-rate-card.component.html',
  styleUrl: './consortium-ocupation-rate-card.component.css',
  standalone: true
})
export class ConsortiumOcupationRateCardComponent {
  @Input() occupancy!: OccupancyMetrics;

  getOwnerPercentage(): number {
    return Math.round((this.occupancy.occupied / this.occupancy.total) * 100);
  }

  getTenantPercentage(): number {
    return Math.round((this.occupancy.rented / this.occupancy.total) * 100);
  }

  getEmptyPercentage(): number {
    return Math.round((this.occupancy.empty / this.occupancy.total) * 100);
  }
}
