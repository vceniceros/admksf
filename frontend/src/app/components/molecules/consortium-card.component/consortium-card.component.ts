import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Consortium } from '../../../../models/consortium.model';
import { CardImageComponent } from '../../atoms/card-image.component/card-image.component';
import { LabelComponent } from '../../atoms/label.component/label.component';
import { StatusLabelComponent } from '../../atoms/status-label.component/status-label.component';
import { InfoRowComponent } from '../info-row.component/info-row.component';
import { IconComponent } from '../../atoms/icon.component/icon.component';

@Component({
  selector: 'app-consortium-card',
  imports: [
    CommonModule,
    CardImageComponent,
    LabelComponent,
    StatusLabelComponent,
    InfoRowComponent,
    IconComponent
  ],
  templateUrl: './consortium-card.component.html',
  styleUrl: './consortium-card.component.css',
  standalone: true
})
export class ConsortiumCardComponent {
  @Input() consortium!: Consortium;
}
