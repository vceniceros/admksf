import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { Consortium } from '../../models/consortium.model';
import { ConsortiumStatus } from '../../models/consortium.model';

@Injectable({
  providedIn: 'root'
})
export class ConsortiumService {
  private apiUrl = '/api/consorcios/';
  private fallbackImage = 'assets/img/complejo-los-alamos.jpg';

  constructor(private http: HttpClient) { }

  getAllConsortiums(): Observable<Consortium[]> {
    return this.http.get<{ status: string; data: any[] }>(this.apiUrl).pipe(
      map(response => (response.data || []).map(item => this.mapConsortium(item)))
    );
  }

  getConsortiumById(id: string): Observable<Consortium | undefined> {
    const cuit = String(id);
    return this.http.get<{ status: string; data: any }>(`${this.apiUrl}${cuit}/`).pipe(
      map(response => (response?.data ? this.mapConsortium(response.data) : undefined))
    );
  }

  getConsortiumDetail(cuit: string | number): Observable<any> {
    return this.http.get<{ status: string; data: any }>(`${this.apiUrl}${cuit}/`).pipe(
      map(response => response?.data)
    );
  }

  createConsortium(payload: any): Observable<any> {
    return this.http.post(`${this.apiUrl}crear/`, payload);
  }

  updateConsortium(cuit: string | number, payload: any): Observable<any> {
    return this.http.put(`${this.apiUrl}${cuit}/actualizar/`, payload);
  }

  deleteConsortium(cuit: string | number): Observable<any> {
    return this.http.delete(`${this.apiUrl}${cuit}/eliminar/`);
  }

  uploadConsortiumImage(cuit: string | number, file: File): Observable<any> {
    const formData = new FormData();
    formData.append('image', file);
    return this.http.post(`${this.apiUrl}${cuit}/imagen/`, formData);
  }

  private mapConsortium(item: any): Consortium {
    const address = item.calle
      ? `${item.calle} ${item.numero ?? ''}, ${item.ciudad ?? ''}`.trim()
      : (item.address || 'Sin dirección');

    return {
      id: String(item.cuit ?? item.id ?? ""),
      name: item.razon_social ?? item.name ?? 'Consorcio sin nombre',
      status: (item.status as ConsortiumStatus) ?? ConsortiumStatus.ACTIVE,
      address,
      units: Number(item.units ?? 0),
      owners: Number(item.owners ?? 0),
      imageUrl: item.imagen_url ?? item.image_url ?? item.imageUrl ?? this.fallbackImage
    };
  }
}
