import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CollectionMetrics } from '../../../../models/dashboardSummary.model';
import { IconComponent } from '../../atoms/icon.component/icon.component';
import { LabelComponent } from '../../atoms/label.component/label.component';
import { PorcentageBarComponent } from '../../atoms/porcentage-bar.component/porcentage-bar.component';

@Component({
  selector: 'app-consortium-collection-rates-card',
  imports: [CommonModule, IconComponent, LabelComponent, PorcentageBarComponent],
  templateUrl: './consortium-collection-rates-card.component.html',
  styleUrl: './consortium-collection-rates-card.component.css',
  standalone: true
})
export class ConsortiumCollectionRatesCardComponent {
  @Input() collection!: CollectionMetrics;
}
