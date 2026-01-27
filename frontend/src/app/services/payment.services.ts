import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Payment } from '../../models/payment.model';

@Injectable({
  providedIn: 'root'
})
export class PaymentService {
  private jsonUrl = 'assets/data/lastPayments.json';

  constructor(private http: HttpClient) { }

  getLastPayments(consortiumId: number): Observable<Payment[]> {
    // Por ahora consume el JSON estático
    // Más adelante consumirá del backend con el consortiumId
    return this.http.get<Payment[]>(this.jsonUrl);
  }
}
