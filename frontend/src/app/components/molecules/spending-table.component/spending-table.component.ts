import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Spend, EstadoPago } from '../../../../models/spends.model';
import { LabelComponent } from '../../atoms/label.component/label.component';
import { IconComponent } from '../../atoms/icon.component/icon.component';
import { PaymentStatusToggleComponent } from '../payment-status-toggle.component/payment-status-toggle.component';

@Component({
  selector: 'app-spending-table',
  imports: [CommonModule, LabelComponent, IconComponent, PaymentStatusToggleComponent],
  templateUrl: './spending-table.component.html',
  styleUrl: './spending-table.component.css',
  standalone: true
})
export class SpendingTableComponent {
  @Input() spends!: Spend[];
  @Input() ordenActual: string = 'periodo';
  @Input() direccion: 'asc' | 'desc' = 'desc';
  @Output() ordenar = new EventEmitter<string>();
  @Output() statusChanged = new EventEmitter<{ spend: Spend; newStatus: EstadoPago }>();
  @Output() editSpend = new EventEmitter<Spend>();
  @Output() deleteSpend = new EventEmitter<Spend>();
  
  EstadoPago = EstadoPago;

  formatMonth(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-AR', { month: 'long', year: 'numeric' });
  }

  formatDateTime(timestampString: string): string {
    const date = new Date(timestampString);
    return date.toLocaleDateString('es-AR', { 
      day: '2-digit', 
      month: '2-digit', 
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
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

  onStatusChanged(event: { spend: Spend; newStatus: EstadoPago }): void {
    this.statusChanged.emit(event);
  }

  onEdit(spend: Spend) {
    this.editSpend.emit(spend);
  }

  onDelete(spend: Spend) {
    this.deleteSpend.emit(spend);
  }
}
