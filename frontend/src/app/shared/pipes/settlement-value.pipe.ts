import { CurrencyPipe } from '@angular/common';
import { Pipe, PipeTransform, inject } from '@angular/core';
import { SettlementColumn } from '../../../models/settlement.model';

@Pipe({
  name: 'settlementValue',
  standalone: true
})
export class SettlementValuePipe implements PipeTransform {
  private currencyPipe = inject(CurrencyPipe);

  transform(value: string | number | null | undefined, column?: SettlementColumn): string {
    if (value === null || value === undefined || value === '') {
      return '-';
    }

    const numericValue = Number(value);
    const shouldFormat = this.isMonetaryColumn(column);

    if (shouldFormat && !Number.isNaN(numericValue)) {
      return (
        this.currencyPipe.transform(numericValue, 'ARS', 'symbol', '1.2-2', 'es-AR') ??
        numericValue.toFixed(2)
      );
    }

    return String(value);
  }

  private isMonetaryColumn(column?: SettlementColumn): boolean {
    if (!column) {
      return false;
    }
    const calcType = (column.calc_type || '').toLowerCase();
    if ([
      'saldo_anterior',
      'interes',
      'prorrateo',
      'concepto_particular',
      'fijo',
      'formula'
    ].includes(calcType)) {
      return true;
    }

    const label = `${column.label ?? ''} ${column.id ?? ''}`.toLowerCase();
    return /monto|total|saldo|inter[eé]s|gasto|expensa|mora|repar|multa/.test(label);
  }
}
