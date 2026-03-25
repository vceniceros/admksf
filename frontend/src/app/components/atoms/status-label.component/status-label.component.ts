import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ConsortiumStatus } from '../../../../models/consortium.model';

@Component({
  selector: 'app-status-label',
  imports: [CommonModule],
  templateUrl: './status-label.component.html',
  styleUrl: './status-label.component.css',
  standalone: true
})
export class StatusLabelComponent {
  @Input() status!: ConsortiumStatus;

  getStatusText(): string {
    switch (this.status) {
      case ConsortiumStatus.ACTIVE:
        return 'Activo';
      case ConsortiumStatus.INACTIVE:
        return 'Inactivo';
      case ConsortiumStatus.PENDING:
        return 'Pendiente';
      default:
        return '';
    }
  }

  getStatusClass(): string {
    switch (this.status) {
      case ConsortiumStatus.ACTIVE:
        return 'status-active';
      case ConsortiumStatus.INACTIVE:
        return 'status-inactive';
      case ConsortiumStatus.PENDING:
        return 'status-pending';
      default:
        return '';
    }
  }
}
