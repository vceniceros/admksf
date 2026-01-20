import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Spend, EstadoPago } from '../../../../models/spends.model';
import { AlertComponent, AlertType } from '../../atoms/alert.component/alert.component';
import { IconComponent } from '../../atoms/icon.component/icon.component';

@Component({
  selector: 'app-payment-status-toggle',
  imports: [CommonModule, AlertComponent, IconComponent],
  templateUrl: './payment-status-toggle.component.html',
  styleUrl: './payment-status-toggle.component.css',
  standalone: true
})
export class PaymentStatusToggleComponent {
  @Input() spend!: Spend;
  @Output() statusChanged = new EventEmitter<{ spend: Spend; newStatus: EstadoPago }>();

  showAlert: boolean = false;
  EstadoPago = EstadoPago;
  AlertType = AlertType;

  onStatusClick(): void {
    this.showAlert = true;
  }

  onConfirmStatusChange(): void {
    const newStatus = this.spend.estadoPago === EstadoPago.PAGADO 
      ? EstadoPago.PENDIENTE 
      : EstadoPago.PAGADO;
    
    this.statusChanged.emit({ spend: this.spend, newStatus });
  }

  onCancelStatusChange(): void {
    this.showAlert = false;
  }

  getAlertMessage(): string {
    if (this.spend.estadoPago === EstadoPago.PENDIENTE) {
      return 'Usted está por confirmar el pago de un servicio.';
    } else {
      return 'Usted está por revertir el pago de un servicio.';
    }
  }

  getConfirmButtonText(): string {
    return this.spend.estadoPago === EstadoPago.PENDIENTE ? 'Confirmar Pago' : 'Revertir Pago';
  }
}
