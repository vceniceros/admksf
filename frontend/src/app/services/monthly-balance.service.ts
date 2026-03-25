import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { MonthlyBalance } from '../../models/monthly-balance.model';

@Injectable({
  providedIn: 'root'
})
export class MonthlyBalanceService {
  private apiUrl = '/api/saldos-mensuales/';

  constructor(private http: HttpClient) {}

  getBalancesByConsortium(cuitConsorcio: string): Observable<MonthlyBalance[]> {
    return this.http.get<{ status: string; data: any[] }>(`${this.apiUrl}consorcio/${cuitConsorcio}/`).pipe(
      map(response => (response.data || []).map(item => this.mapBalance(item)))
    );
  }

  getBalanceById(id: number): Observable<MonthlyBalance | undefined> {
    return this.http.get<{ status: string; data: any }>(`${this.apiUrl}${id}/`).pipe(
      map(response => (response?.data ? this.mapBalance(response.data) : undefined))
    );
  }

  createBalance(payload: any): Observable<any> {
    return this.http.post(`${this.apiUrl}crear/`, payload);
  }

  updateBalance(id: number, payload: any): Observable<any> {
    return this.http.put(`${this.apiUrl}${id}/actualizar/`, payload);
  }

  deleteBalance(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}${id}/eliminar/`);
  }

  private mapBalance(item: any): MonthlyBalance {
    return {
      id: Number(item.id ?? 0),
      numeroUnidad: Number(item.numero_unidad ?? item.numero_de_unidad_funcional ?? 0),
      cuitConsorcio: String(item.consorcio ?? item.cuit_consorcio ?? ''),
      mesAnio: item.mes_anio ?? '',
      saldoInicial: Number(item.saldo_inicial ?? 0),
      totalGastos: Number(item.total_gastos ?? 0),
      totalPagos: Number(item.total_pagos ?? 0),
      saldoFinal: Number(item.saldo_final ?? 0),
      fechaCierre: item.fecha_cierre ?? null
    };
  }
}
