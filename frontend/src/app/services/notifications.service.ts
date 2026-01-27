import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Notification } from '../../models/notifications.model';

@Injectable({
  providedIn: 'root'
})
export class NotificationsService {
  private jsonUrl = 'assets/data/notificacions.json';

  constructor(private http: HttpClient) { }

  getNotifications(consortiumId: number): Observable<Notification[]> {
    // Por ahora consume el JSON estático
    // Más adelante consumirá del backend con el consortiumId
    return this.http.get<Notification[]>(this.jsonUrl);
  }
}
