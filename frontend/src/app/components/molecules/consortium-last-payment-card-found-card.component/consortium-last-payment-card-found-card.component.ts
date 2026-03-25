import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Payment } from '../../../../models/payment.model';
import { IconComponent } from '../../atoms/icon.component/icon.component';
import { LabelComponent } from '../../atoms/label.component/label.component';

@Component({
  selector: 'app-consortium-last-payment-card-found-card',
  imports: [CommonModule, IconComponent, LabelComponent],
  templateUrl: './consortium-last-payment-card-found-card.component.html',
  styleUrl: './consortium-last-payment-card-found-card.component.css',
  standalone: true
})
export class ConsortiumLastPaymentCardFoundCardComponent {
  @Input() payments!: Payment[];
}
