import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { ServiceStatusItem } from '../../models/services.model';

@Injectable({
  providedIn: 'root'
})
export class ServicesService {
  private apiUrl = '/api/servicios-mensuales/';

  constructor(private http: HttpClient) { }

  getServicesStatus(consortiumId: number | string): Observable<ServiceStatusItem[]> {
    return this.http.get<{ status: string; data: any[] }>(this.apiUrl).pipe(
      map(response => (response.data || []).map(item => this.mapServiceItem(item)))
    );
  }

  private mapServiceItem(item: any): ServiceStatusItem {
    return {
      id: String(item.cuit ?? item.razon_social ?? 'service'),
      name: item.razon_social ?? 'Servicio Mensual',
      company: item.razon_social ?? 'Proveedor',
      phoneNumber: item.numero_reclamo ?? item.numero_cuenta ?? '-',
      status: 'OK'
    };
  }
}
