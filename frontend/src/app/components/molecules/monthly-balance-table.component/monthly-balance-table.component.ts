import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MonthlyBalance } from '../../../../models/monthly-balance.model';
import { LabelComponent } from '../../atoms/label.component/label.component';
import { IconComponent } from '../../atoms/icon.component/icon.component';

@Component({
  selector: 'app-monthly-balance-table',
  imports: [CommonModule, LabelComponent, IconComponent],
  templateUrl: './monthly-balance-table.component.html',
  styleUrls: ['./monthly-balance-table.component.css'],
  standalone: true
})
export class MonthlyBalanceTableComponent {
  @Input() balances: MonthlyBalance[] = [];
  @Output() editBalance = new EventEmitter<MonthlyBalance>();
  @Output() deleteBalance = new EventEmitter<MonthlyBalance>();

  onEdit(balance: MonthlyBalance) {
    this.editBalance.emit(balance);
  }

  onDelete(balance: MonthlyBalance) {
    this.deleteBalance.emit(balance);
  }

  formatDate(value: string) {
    const date = new Date(value);
    return date.toLocaleDateString('es-AR', { month: 'long', year: 'numeric' });
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
