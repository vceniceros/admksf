import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { Consortium } from '../../models/consortium.model';

@Injectable({
  providedIn: 'root'
})
export class ConsortiumService {
  private jsonUrl = 'assets/data/consorciosTest.json';

  constructor(private http: HttpClient) { }

  getAllConsortiums(): Observable<Consortium[]> {
    // Por ahora consume el JSON estático
    // Más adelante consumirá del backend cambiando la URL
    return this.http.get<Consortium[]>(this.jsonUrl);
  }

  getConsortiumById(id: number): Observable<Consortium | undefined> {
    return this.getAllConsortiums().pipe(
      map(consortia => consortia.find(c => c.id === id))
    );
  }
}
