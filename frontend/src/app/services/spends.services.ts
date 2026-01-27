import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map, of, BehaviorSubject } from 'rxjs';
import { Spend, EstadoPago } from '../../models/spends.model';

@Injectable({
  providedIn: 'root'
})
export class SpendsService {
  private jsonUrl = 'assets/data/spendsTest.json';
  private localSpends: Spend[] = [];
  private spendsSubject = new BehaviorSubject<Spend[]>([]);

  constructor(private http: HttpClient) { }

  getAllSpends(): Observable<Spend[]> {
    // Por ahora consume el JSON estático
    // Más adelante consumirá del backend cambiando la URL
    return this.http.get<Spend[]>(this.jsonUrl).pipe(
      map(jsonSpends => {
        // Combina los gastos del JSON con los gastos locales (agregados en memoria)
        const allSpends = [...jsonSpends, ...this.localSpends];
        return allSpends;
      })
    );
  }

  getSpendById(id: number): Observable<Spend | undefined> {
    return this.getAllSpends().pipe(
      map(spends => spends.find(s => s.idGasto === id))
    );
  }

  addSpend(spend: Spend): Observable<Spend> {
    // Por ahora simula agregar el gasto (en memoria para pruebas)
    // Más adelante se conectará al backend para guardar realmente
    this.localSpends = [...this.localSpends, spend];
    return of(spend);
  }

  updateSpendStatus(spend: Spend, newStatus: EstadoPago): Observable<Spend> {
    // Actualiza el estado del gasto
    // API: POST /api/gastos/{idGasto}/status
    // Por ahora solo actualiza en memoria
    const updatedSpend = { ...spend, estadoPago: newStatus };
    
    // Actualizar en localSpends si existe
    const localIndex = this.localSpends.findIndex(s => s.idGasto === spend.idGasto);
    if (localIndex !== -1) {
      this.localSpends[localIndex] = updatedSpend;
    }
    
    // TODO: Reemplazar con llamada real al backend
    // return this.http.post<Spend>(`/api/gastos/${spend.idGasto}/status`, { estadoPago: newStatus });
    
    return of(updatedSpend);
  }
}

