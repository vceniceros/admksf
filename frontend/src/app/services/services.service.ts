import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ServiceStatusItem } from '../../models/services.model';

@Injectable({
  providedIn: 'root'
})
export class ServicesService {
  private jsonUrl = 'assets/data/servicesStatus.json';

  constructor(private http: HttpClient) { }

  getServicesStatus(consortiumId: number): Observable<ServiceStatusItem[]> {
    // Por ahora consume el JSON estático
    // Más adelante consumirá del backend con el consortiumId
    return this.http.get<ServiceStatusItem[]>(this.jsonUrl);
  }
}
