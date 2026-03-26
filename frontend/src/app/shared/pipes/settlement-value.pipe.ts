import { formatCurrency } from '@angular/common';
import { Pipe, PipeTransform, LOCALE_ID, inject } from '@angular/core';
import { SettlementColumn } from '../../../models/settlement.model';

@Pipe({
  name: 'settlementValue',
  standalone: true
})
export class SettlementValuePipe implements PipeTransform {
  private locale = inject(LOCALE_ID);

  transform(value: string | number | null | undefined, column?: SettlementColumn): string {
    if (value === null || value === undefined || value === '') {
      return '-';
    }
    const numericValue = Number(value);
    if (this.isMonetaryColumn(column) && !Number.isNaN(numericValue)) {
      return formatCurrency(numericValue, this.locale, '$', 'ARS', '1.2-2');
    }
    return String(value);
  }

  private isMonetaryColumn(column?: SettlementColumn): boolean {
    if (!column) return false;
    const calcType = (column.calc_type || '').toLowerCase();
    if (['saldo_anterior','interes','prorrateo','concepto_particular','fijo','formula'].includes(calcType)) {
      return true;
    }
    const label = `${column.label ?? ''} ${column.id ?? ''}`.toLowerCase();
    return /monto|total|saldo|inter[eé]s|gasto|expensa|mora|repar|multa/.test(label);
  }
}
