import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { Spend, EstadoPago } from '../../models/spends.model';

@Injectable({
  providedIn: 'root'
})
export class SpendsService {
  private apiUrl = '/api/gastos/';

  constructor(private http: HttpClient) { }

  getAllSpends(): Observable<Spend[]> {
    return this.http.get<{ status: string; data: any[] }>(this.apiUrl).pipe(
      map(response => (response.data || []).map(item => this.mapSpend(item)))
    );
  }

  getSpendsByConsortium(cuitConsorcio: string): Observable<Spend[]> {
    return this.http.get<{ status: string; data: any[] }>(`${this.apiUrl}consorcio/${cuitConsorcio}/`).pipe(
      map(response => (response.data || []).map(item => this.mapSpend(item)))
    );
  }

  getSpendById(id: number): Observable<Spend | undefined> {
    return this.http.get<{ status: string; data: any }>(`${this.apiUrl}${id}/`).pipe(
      map(response => (response?.data ? this.mapSpend(response.data) : undefined))
    );
  }

  addSpend(payload: any): Observable<any> {
    return this.http.post(`${this.apiUrl}crear/`, payload);
  }

  addSpendFromFile(payload: any, file: File): Observable<any> {
    const formData = new FormData();
    formData.append('archivo', file);
    Object.entries(payload || {}).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        formData.append(key, String(value));
      }
    });
    return this.http.post(`${this.apiUrl}cargar-desde-archivo/`, formData);
  }

  extractSpendFromFile(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('archivo', file);
    return this.http.post(`${this.apiUrl}extraer-desde-archivo/`, formData);
  }

  updateSpendStatus(spend: Spend, newStatus: EstadoPago): Observable<any> {
    return this.http.put(`${this.apiUrl}${spend.idGasto}/actualizar/`, {
      estado_pago: newStatus
    });
  }

  updateSpend(id: number, payload: any): Observable<any> {
    return this.http.put(`${this.apiUrl}${id}/actualizar/`, payload);
  }

  deleteSpend(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}${id}/eliminar/`);
  }

  private mapSpend(item: any): Spend {
    return {
      idGasto: Number(item.id ?? item.id_gasto ?? 0),
      cuitConsorcio: String(item.consorcio ?? item.cuit_consorcio ?? ''),
      cuitProveedor: String(item.proveedor ?? item.cuit_proveedor ?? ''),
      periodo: item.periodo ?? '',
      descripcion: item.descripcion ?? '',
      monto: Number(item.monto ?? 0),
      fechaRegistro: item.fecha_registro ?? '',
      tipoGasto: item.tipo_gasto ?? item.tipoGasto ?? item.tipo ?? '',
      estadoPago: item.estado_pago ?? item.estadoPago ?? item.estado ?? ''
    } as Spend;
  }
}

