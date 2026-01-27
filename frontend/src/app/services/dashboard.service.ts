import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { DashboardSummary } from '../../models/dashboardSummary.model';

@Injectable({
  providedIn: 'root'
})
export class DashboardService {
  private jsonUrl = 'assets/data/dashboardSummary.json';

  constructor(private http: HttpClient) { }

  getDashboardSummary(consortiumId: number): Observable<DashboardSummary> {
    // Por ahora consume el JSON estático
    // Más adelante consumirá del backend con el consortiumId
    return this.http.get<DashboardSummary>(this.jsonUrl);
  }
}
