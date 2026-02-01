import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { Unit } from '../../models/unit.model';

@Injectable({
  providedIn: 'root'
})
export class UnitsService {
  private apiUrl = '/api/unidades-funcionales/';

  constructor(private http: HttpClient) {}

  getAllUnits(): Observable<Unit[]> {
    return this.http.get<{ status: string; data: any[] }>(this.apiUrl).pipe(
      map(response => (response.data || []).map(item => this.mapUnit(item)))
    );
  }

  getUnitsByConsortium(cuit: string | number): Observable<Unit[]> {
    return this.http.get<{ status: string; data: any[] }>(`${this.apiUrl}consorcio/${cuit}/`).pipe(
      map(response => (response.data || []).map(item => this.mapUnit(item)))
    );
  }

  getUnitsByOwner(dni: string): Observable<Unit[]> {
    return this.http.get<{ status: string; data: any[] }>(`${this.apiUrl}propietario/${dni}/`).pipe(
      map(response => (response.data || []).map(item => this.mapUnit(item)))
    );
  }

  getUnitByNumber(numero: number): Observable<Unit | undefined> {
    return this.http.get<{ status: string; data: any }>(`${this.apiUrl}${numero}/`).pipe(
      map(response => (response?.data ? this.mapUnit(response.data) : undefined))
    );
  }

  createUnit(payload: any): Observable<any> {
    return this.http.post(`${this.apiUrl}crear/`, payload);
  }

  updateUnit(numero: number, payload: any): Observable<any> {
    return this.http.put(`${this.apiUrl}${numero}/actualizar/`, payload);
  }

  deleteUnit(numero: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}${numero}/eliminar/`);
  }

  private mapUnit(item: any): Unit {
    return {
      numero: Number(item.numero ?? item.numero_de_unidad_funcional ?? 0),
      consorcio: String(item.consorcio ?? ''),
      tipo_de_unidad: item.tipo_de_unidad ?? item.tipo ?? '',
      estado_de_vivienda: item.estado_de_vivienda ?? item.estado ?? '',
      superficie: String(item.superficie ?? ''),
      propietario: item.propietario ?? null
    };
  }
}
