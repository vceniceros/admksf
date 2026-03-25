import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, forkJoin, map } from 'rxjs';
import { DashboardSummary } from '../../models/dashboardSummary.model';

@Injectable({
  providedIn: 'root'
})
export class DashboardService {
  private paymentsUrl = '/api/pagos/consorcio/';
  private expensesUrl = '/api/gastos/consorcio/';
  private unitsUrl = '/api/unidades-funcionales/consorcio/';

  constructor(private http: HttpClient) { }

  getDashboardSummary(consortiumId: number | string): Observable<DashboardSummary> {
    return forkJoin({
      payments: this.http.get<{ status: string; data: any[] }>(`${this.paymentsUrl}${consortiumId}/`),
      expenses: this.http.get<{ status: string; data: any[] }>(`${this.expensesUrl}${consortiumId}/`),
      units: this.http.get<{ status: string; data: any[] }>(`${this.unitsUrl}${consortiumId}/`)
    }).pipe(
      map(({ payments, expenses, units }) => {
        const now = new Date();
        const currentMonth = now.getMonth();
        const currentYear = now.getFullYear();

        const previousMonthDate = new Date(currentYear, currentMonth - 1, 1);
        const previousMonth = previousMonthDate.getMonth();
        const previousYear = previousMonthDate.getFullYear();

        const paymentItems = payments?.data || [];
        const expenseItems = expenses?.data || [];
        const unitItems = units?.data || [];

        const monthlyIncome = this.sumByMonth(paymentItems, 'fecha_pago', currentMonth, currentYear, ['Aprobado', 'Parcial']);
        const previousIncome = this.sumByMonth(paymentItems, 'fecha_pago', previousMonth, previousYear, ['Aprobado', 'Parcial']);

        const monthlyExpenses = this.sumByMonth(expenseItems, 'periodo', currentMonth, currentYear);
        const previousExpenses = this.sumByMonth(expenseItems, 'periodo', previousMonth, previousYear);

        const incomeTrend = this.calculateTrend(monthlyIncome, previousIncome);
        const expenseTrend = this.calculateTrend(monthlyExpenses, previousExpenses);

        const pendingAmount = Math.max(monthlyExpenses - monthlyIncome, 0);
        const percentage = monthlyExpenses > 0
          ? Math.round((monthlyIncome / monthlyExpenses) * 100)
          : 100;

        const totalUnits = unitItems.length;
        const emptyUnits = unitItems.filter((u: any) => String(u.estado_de_vivienda || '').toLowerCase() === 'vacio').length;
        const rentedUnits = unitItems.filter((u: any) => String(u.estado_de_vivienda || '').toLowerCase() === 'inquilino').length;
        const occupiedUnits = Math.max(totalUnits - emptyUnits, 0);

        return {
          consortiumId: Number(consortiumId),
          financials: {
            monthlyIncome,
            monthlyExpenses,
            incomeTrend,
            expenseTrend
          },
          collection: {
            percentage,
            collectedAmount: monthlyIncome,
            pendingAmount
          },
          occupancy: {
            total: totalUnits,
            occupied: occupiedUnits,
            rented: rentedUnits,
            empty: emptyUnits
          }
        };
      })
    );
  }

  private sumByMonth(items: any[], dateField: string, month: number, year: number, allowedStatuses?: string[]): number {
    return items.reduce((total, item) => {
      const rawDate = item?.[dateField];
      if (!rawDate) {
        return total;
      }

      const date = new Date(rawDate);
      if (Number.isNaN(date.getTime())) {
        return total;
      }

      if (date.getMonth() !== month || date.getFullYear() !== year) {
        return total;
      }

      if (allowedStatuses && !allowedStatuses.includes(String(item?.estado_pago))) {
        return total;
      }

      return total + Number(item?.monto || 0);
    }, 0);
  }

  private calculateTrend(current: number, previous: number): number {
    if (previous <= 0) {
      return 0;
    }
    return Math.round(((current - previous) / previous) * 100);
  }
}
