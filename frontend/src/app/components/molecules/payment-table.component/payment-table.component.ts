import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Payment } from '../../../../models/payment.model';
import { LabelComponent } from '../../atoms/label.component/label.component';
import { IconComponent } from '../../atoms/icon.component/icon.component';

@Component({
  selector: 'app-payment-table',
  imports: [CommonModule, LabelComponent, IconComponent],
  templateUrl: './payment-table.component.html',
  styleUrl: './payment-table.component.css',
  standalone: true
})
export class PaymentTableComponent {
  @Input() payments: Payment[] = [];
  @Output() emailClicked = new EventEmitter<Payment>();
  @Output() editClicked = new EventEmitter<Payment>();
  @Output() rejectClicked = new EventEmitter<Payment>();

  onEmail(payment: Payment) {
    this.emailClicked.emit(payment);
  }

  onEdit(payment: Payment) {
    this.editClicked.emit(payment);
  }

  onReject(payment: Payment) {
    this.rejectClicked.emit(payment);
  }

  formatDate(value?: string) {
    if (!value) {
      return '-';
    }
    const date = new Date(value);
    return date.toLocaleDateString('es-AR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  }

  formatCurrency(amount: number): string {
    return new Intl.NumberFormat('es-AR', {
      style: 'currency',
      currency: 'ARS',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(amount);
  }

  getStatusLabel(status: string) {
    return status;
  }
}
