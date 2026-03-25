import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { Owner } from '../../models/owner.model';

@Injectable({
  providedIn: 'root'
})
export class OwnersService {
  private apiUrl = '/api/propietarios/';

  constructor(private http: HttpClient) {}

  getAllOwners(): Observable<Owner[]> {
    return this.http.get<{ status: string; data: any[] }>(this.apiUrl).pipe(
      map(response => (response.data || []).map(item => this.mapOwner(item)))
    );
  }

  getOwnerByDni(dni: string): Observable<Owner | undefined> {
    return this.http.get<{ status: string; data: any }>(`${this.apiUrl}${dni}/`).pipe(
      map(response => (response?.data ? this.mapOwner(response.data) : undefined))
    );
  }

  createOwner(payload: Owner): Observable<any> {
    return this.http.post(`${this.apiUrl}crear/`, payload);
  }

  updateOwner(dni: string, payload: Partial<Owner>): Observable<any> {
    return this.http.put(`${this.apiUrl}${dni}/actualizar/`, payload);
  }

  deleteOwner(dni: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}${dni}/eliminar/`);
  }

  private mapOwner(item: any): Owner {
    return {
      dni: String(item.dni ?? ''),
      nombre: item.nombre ?? '',
      apellido: item.apellido ?? '',
      telefono: item.telefono ?? null,
      email: item.email ?? null
    };
  }
}
