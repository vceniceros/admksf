import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Event } from '../../../../models/event.model';
import { IconComponent } from '../../atoms/icon.component/icon.component';
import { LabelComponent } from '../../atoms/label.component/label.component';
import { GenericButtonComponent } from '../../atoms/generic-button.component/generic-button.component';

@Component({
  selector: 'app-consortium-events-card',
  imports: [CommonModule, FormsModule, IconComponent, LabelComponent, GenericButtonComponent],
  templateUrl: './consortium-events-card.component.html',
  styleUrl: './consortium-events-card.component.css',
  standalone: true
})
export class ConsortiumEventsCardComponent {
  @Input() events!: Event[];
  
  showForm: boolean = false;
  newEventDate: string = '';
  newEventDescription: string = '';

  toggleForm(): void {
    this.showForm = !this.showForm;
    if (!this.showForm) {
      this.resetForm();
    }
  }

  addEvent(): void {
    if (this.newEventDate && this.newEventDescription) {
      const newEvent: Event = {
        id: this.events.length + 1,
        date: this.formatDate(this.newEventDate),
        description: this.newEventDescription
      };
      
      this.events.unshift(newEvent);
      this.resetForm();
      this.showForm = false;
    }
  }

  formatDate(dateString: string): string {
    const date = new Date(dateString);
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    return `${day}/${month}/${year}`;
  }

  resetForm(): void {
    this.newEventDate = '';
    this.newEventDescription = '';
  }
}
