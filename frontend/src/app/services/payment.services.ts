import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { Payment } from '../../models/payment.model';

@Injectable({
  providedIn: 'root'
})
export class PaymentService {
  private apiUrl = '/api/pagos/';

  constructor(private http: HttpClient) { }

  getLastPayments(consortiumId: number | string): Observable<Payment[]> {
    return this.http.get<{ status: string; data: any[] }>(`${this.apiUrl}consorcio/${consortiumId}/`).pipe(
      map(response => {
        const mapped = (response.data || []).map(item => this.mapBackendPayment(item));
        return mapped
          .sort((a, b) => this.parseDate(b.fechaPago) - this.parseDate(a.fechaPago))
          .slice(0, 5);
      })
    );
  }

  getPaymentsByConsortium(cuitConsorcio: string): Observable<Payment[]> {
    return this.http.get<{ status: string; data: any[] }>(`${this.apiUrl}consorcio/${cuitConsorcio}/`).pipe(
      map(response => (response.data || []).map(item => this.mapBackendPayment(item)))
    );
  }

  getPaymentById(id: number): Observable<Payment | undefined> {
    return this.http.get<{ status: string; data: any }>(`${this.apiUrl}${id}/`).pipe(
      map(response => (response?.data ? this.mapBackendPayment(response.data) : undefined))
    );
  }

  createPayment(payload: any): Observable<any> {
    return this.http.post(`${this.apiUrl}crear/`, payload);
  }

  updatePayment(id: number, payload: any): Observable<any> {
    return this.http.put(`${this.apiUrl}${id}/actualizar/`, payload);
  }

  deletePayment(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}${id}/eliminar/`);
  }

  private mapBackendPayment(item: any): Payment {
    const numeroUnidad = item.numero_unidad ?? item.numero_de_unidad_funcional;
    const propietario = item.propietario ?? item.dni_propietario;
    return {
      id: Number(item.id ?? 0),
      amount: Number(item.monto ?? 0),
      status: item.estado_pago ?? 'Pendiente',
      personName: propietario ? String(propietario) : undefined,
      unit: numeroUnidad ? `UF ${numeroUnidad}` : undefined,
      numeroUnidad,
      cuitConsorcio: item.consorcio ?? item.cuit_consorcio,
      propietario,
      fechaPago: item.fecha_pago ?? ''
    };
  }

  private parseDate(dateValue?: string): number {
    if (!dateValue) {
      return 0;
    }
    const parsed = new Date(dateValue).getTime();
    return Number.isNaN(parsed) ? 0 : parsed;
  }
}
