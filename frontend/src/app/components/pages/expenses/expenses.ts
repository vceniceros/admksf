import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { SpendsService } from '../../../services/spends.services';
import { Spend, EstadoPago } from '../../../../models/spends.model';
import { LabelComponent } from '../../atoms/label.component/label.component';
import { IconComponent } from '../../atoms/icon.component/icon.component';
import { SpendingTableComponent } from '../../molecules/spending-table.component/spending-table.component';

@Component({
  selector: 'app-expenses',
  imports: [CommonModule, RouterModule, LabelComponent, IconComponent, SpendingTableComponent],
  templateUrl: './expenses.html',
  styleUrl: './expenses.css',
  standalone: true
})
export class Expenses implements OnInit {
  consortiumName: string = '';
  spends: Spend[] = [];
  
  totalSpends: number = 0;
  paidSpends: number = 0;
  pendingSpends: number = 0;

  constructor(
    private route: ActivatedRoute,
    private spendsService: SpendsService
  ) {}

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.consortiumName = params['consortiumName'];
      this.loadSpends();
    });
  }

  loadSpends() {
    this.spendsService.getAllSpends().subscribe({
      next: (data: Spend[]) => {
        this.spends = data;
        this.calculateBalances();
      },
      error: (error: any) => {
        console.error('Error loading spends:', error);
      }
    });
  }

  calculateBalances() {
    this.totalSpends = this.spends.reduce((sum, spend) => sum + spend.monto, 0);
    this.paidSpends = this.spends
      .filter(spend => spend.estadoPago === EstadoPago.PAGADO)
      .reduce((sum, spend) => sum + spend.monto, 0);
    this.pendingSpends = this.spends
      .filter(spend => spend.estadoPago === EstadoPago.PENDIENTE)
      .reduce((sum, spend) => sum + spend.monto, 0);
  }

  onStatusChanged(event: { spend: Spend; newStatus: EstadoPago }): void {
    this.spendsService.updateSpendStatus(event.spend, event.newStatus).subscribe({
      next: (updatedSpend: Spend) => {
        // Actualizar el gasto en la lista local
        const index = this.spends.findIndex(s => s.idGasto === updatedSpend.idGasto);
        if (index !== -1) {
          this.spends[index] = updatedSpend;
          // Recalcular balances
          this.calculateBalances();
        }
      },
      error: (error: any) => {
        console.error('Error updating spend status:', error);
      }
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
}
