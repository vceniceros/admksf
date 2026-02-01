import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { Provider } from '../../models/provider.model';

@Injectable({
  providedIn: 'root'
})
export class ProvidersService {
  private apiUrl = '/api/proveedores/';
  private serviciosUrl = '/api/servicios-mensuales/';
  private reparacionesUrl = '/api/reparaciones-mantenimientos/';

  constructor(private http: HttpClient) {}

  getAllProviders(): Observable<Provider[]> {
    return this.http.get<{ status: string; data: any[] }>(this.apiUrl).pipe(
      map(response => (response.data || []).map(item => this.mapProvider(item)))
    );
  }

  getProviderByCuit(cuit: string): Observable<Provider | undefined> {
    return this.http.get<{ status: string; data: any }>(`${this.apiUrl}${cuit}/`).pipe(
      map(response => (response?.data ? this.mapProvider(response.data) : undefined))
    );
  }

  createProvider(payload: any): Observable<any> {
    return this.http.post(`${this.apiUrl}crear/`, payload);
  }

  updateProvider(cuit: string, payload: any): Observable<any> {
    return this.http.put(`${this.apiUrl}${cuit}/actualizar/`, payload);
  }

  deleteProvider(cuit: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}${cuit}/eliminar/`);
  }

  getServicioMensual(cuit: string): Observable<any> {
    return this.http.get<{ status: string; data: any }>(`${this.serviciosUrl}${cuit}/`).pipe(
      map(response => response?.data)
    );
  }

  createServicioMensual(payload: any): Observable<any> {
    return this.http.post(`${this.serviciosUrl}crear/`, payload);
  }

  updateServicioMensual(cuit: string, payload: any): Observable<any> {
    return this.http.put(`${this.serviciosUrl}${cuit}/actualizar/`, payload);
  }

  deleteServicioMensual(cuit: string): Observable<any> {
    return this.http.delete(`${this.serviciosUrl}${cuit}/eliminar/`);
  }

  getReparacionMantenimiento(cuit: string): Observable<any> {
    return this.http.get<{ status: string; data: any }>(`${this.reparacionesUrl}${cuit}/`).pipe(
      map(response => response?.data)
    );
  }

  createReparacionMantenimiento(payload: any): Observable<any> {
    return this.http.post(`${this.reparacionesUrl}crear/`, payload);
  }

  updateReparacionMantenimiento(cuit: string, payload: any): Observable<any> {
    return this.http.put(`${this.reparacionesUrl}${cuit}/actualizar/`, payload);
  }

  deleteReparacionMantenimiento(cuit: string): Observable<any> {
    return this.http.delete(`${this.reparacionesUrl}${cuit}/eliminar/`);
  }

  private mapProvider(item: any): Provider {
    return {
      cuit: String(item.cuit ?? ''),
      razon_social: item.razon_social ?? '',
      telefono: item.telefono ?? null,
      email: item.email ?? null,
      calle: item.calle ?? '',
      numero: Number(item.numero ?? 0),
      codigo_postal: item.codigo_postal ?? '',
      ciudad: item.ciudad ?? '',
      tipo_proveedor: item.tipo_proveedor ?? 'servicios_mensuales',
      numero_cuenta: item.numero_cuenta ?? null,
      numero_reclamo: item.numero_reclamo ?? null
    };
  }
}
