import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { PaymentService } from '../../../services/payment.services';
import { ConsortiumService } from '../../../services/consortium.service';
import { Payment } from '../../../../models/payment.model';
import { LabelComponent } from '../../atoms/label.component/label.component';
import { IconComponent } from '../../atoms/icon.component/icon.component';
import { PaymentTableComponent } from '../../molecules/payment-table.component/payment-table.component';

@Component({
  selector: 'app-payments',
  imports: [CommonModule, LabelComponent, IconComponent, PaymentTableComponent],
  templateUrl: './payments.html',
  styleUrl: './payments.css',
  standalone: true
})
export class Payments implements OnInit {
  consortiumName: string = '';
  consortiumId: string = '';
  payments: Payment[] = [];

  constructor(
    private route: ActivatedRoute,
    private paymentService: PaymentService,
    private consortiumService: ConsortiumService,
    private router: Router
  ) {}

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.consortiumName = params['consortiumName'];
      this.loadConsortiumData();
    });
  }

  loadConsortiumData() {
    this.consortiumService.getAllConsortiums().subscribe({
      next: (consortia) => {
        const decodedName = decodeURIComponent(this.consortiumName.replace(/-/g, ' '));
        const found = consortia.find(c => c.name.toLowerCase() === decodedName.toLowerCase());
        if (found) {
          this.consortiumId = String(found.id);
          this.loadPayments();
        }
      },
      error: (error) => {
        console.error('Error loading consortium:', error);
      }
    });
  }

  loadPayments() {
    if (!this.consortiumId) {
      return;
    }
    this.paymentService.getPaymentsByConsortium(this.consortiumId).subscribe({
      next: (data) => {
        this.payments = data;
      },
      error: (error) => {
        console.error('Error loading payments:', error);
      }
    });
  }

  onEmailClicked(payment: Payment) {
    // TODO: Por ahora no hace nada. Más adelante se integrará con envío de recibo.
    console.log('Email action pending', payment);
  }

  onEditPayment(payment: Payment) {
    this.router.navigate(['/dashboard', this.consortiumName, 'pagos', payment.id, 'editar']);
  }

  onRejectPayment(payment: Payment) {
    this.paymentService.updatePayment(payment.id, { estado_pago: 'Pendiente' }).subscribe({
      next: () => {
        this.loadPayments();
      },
      error: (error) => {
        console.error('Error rejecting payment:', error);
      }
    });
  }

  onAddPayment() {
    this.router.navigate(['/dashboard', this.consortiumName, 'pagos', 'carga-de-pago']);
  }
}
