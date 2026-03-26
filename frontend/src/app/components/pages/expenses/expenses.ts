import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule, Router } from '@angular/router';
import { SpendsService } from '../../../services/spends.services';
import { ConsortiumService } from '../../../services/consortium.service';
import { Spend, EstadoPago } from '../../../../models/spends.model';
import { LabelComponent } from '../../atoms/label.component/label.component';
import { IconComponent } from '../../atoms/icon.component/icon.component';
import { SpendingTableComponent } from '../../molecules/spending-table.component/spending-table.component';
import { switchMap } from 'rxjs';

@Component({
  selector: 'app-expenses',
  imports: [CommonModule, RouterModule, LabelComponent, IconComponent, SpendingTableComponent],
  templateUrl: './expenses.html',
  styleUrl: './expenses.css',
  standalone: true
})
export class Expenses implements OnInit {
  consortiumName: string = '';
  consortiumId: string = '';
  spends: Spend[] = [];

  totalSpends: number = 0;
  paidSpends: number = 0;
  pendingSpends: number = 0;

  showDeleteModal = false;
  spendToDelete: Spend | null = null;

  constructor(
    private route: ActivatedRoute,
    private spendsService: SpendsService,
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
    this.consortiumService.getAllConsortiums().pipe(
      switchMap(consortia => {
        const decodedName = decodeURIComponent(this.consortiumName.replace(/-/g, ' '));
        const found = consortia.find(c => c.name.toLowerCase() === decodedName.toLowerCase());
        if (found) {
          this.consortiumId = String(found.id);
          return this.spendsService.getSpendsByConsortium(this.consortiumId);
        }
        return [];
      })
    ).subscribe({
      next: (data: Spend[]) => {
        this.spends = data;
        this.calculateBalances();
      },
      error: (error) => {
        console.error('Error loading data:', error);
      }
    });
  }

  loadSpends() {
    if (!this.consortiumId) {
      return;
    }
    this.spendsService.getSpendsByConsortium(this.consortiumId).subscribe({
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
      .filter(spend => spend.estadoPago === EstadoPago.APROBADO)
      .reduce((sum, spend) => sum + spend.monto, 0);
    this.pendingSpends = this.spends
      .filter(spend => spend.estadoPago === EstadoPago.PENDIENTE)
      .reduce((sum, spend) => sum + spend.monto, 0);
  }

  onStatusChanged(event: { spend: Spend; newStatus: EstadoPago }): void {
    this.spendsService.updateSpendStatus(event.spend, event.newStatus).subscribe({
      next: () => {
        this.loadSpends();
      },
      error: (error: any) => {
        console.error('Error updating spend status:', error);
      }
    });
  }

  onEditSpend(spend: Spend) {
    this.router.navigate(['/dashboard', this.consortiumName, 'gastos', spend.idGasto, 'editar']);
  }

  onDeleteSpend(spend: Spend) {
    this.spendToDelete = spend;
    this.showDeleteModal = true;
  }

  closeDeleteModal() {
    this.showDeleteModal = false;
    this.spendToDelete = null;
  }

  confirmDelete() {
    if (!this.spendToDelete) {
      return;
    }
    this.spendsService.deleteSpend(this.spendToDelete.idGasto).subscribe({
      next: () => {
        this.closeDeleteModal();
        this.loadSpends();
      },
      error: (error: any) => {
        console.error('Error deleting spend:', error);
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
