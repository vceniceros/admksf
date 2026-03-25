import { Injectable } from '@angular/core';
import { Observable, of, BehaviorSubject } from 'rxjs';
import { Event } from '../../models/event.model';
import eventsData from '../../assets/data/eventsTest.json';

@Injectable({
  providedIn: 'root'
})
export class EventsService {
  private eventsSubject = new BehaviorSubject<Event[]>(eventsData as Event[]);
  
  getEvents(consortiumId: number): Observable<Event[]> {
    return this.eventsSubject.asObservable();
  }

  addEvent(event: Event): void {
    const currentEvents = this.eventsSubject.value;
    this.eventsSubject.next([event, ...currentEvents]);
    
    // Aquí podrías hacer una llamada HTTP para persistir en el backend
    console.log('Evento agregado (solo en memoria):', event);
  }
}
