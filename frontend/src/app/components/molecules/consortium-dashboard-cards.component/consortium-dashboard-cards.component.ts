import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DashboardSummary } from '../../../../models/dashboardSummary.model';
import { Consortium } from '../../../../models/consortium.model';
import { IconComponent } from '../../atoms/icon.component/icon.component';
import { LabelComponent } from '../../atoms/label.component/label.component';

@Component({
  selector: 'app-consortium-dashboard-cards',
  imports: [CommonModule, IconComponent, LabelComponent],
  templateUrl: './consortium-dashboard-cards.component.html',
  styleUrl: './consortium-dashboard-cards.component.css',
  standalone: true
})
export class ConsortiumDashboardCardsComponent {
  @Input() dashboardSummary!: DashboardSummary;
  @Input() consortium!: Consortium;
}
