import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Provider } from '../../../../models/provider.model';
import { LabelComponent } from '../../atoms/label.component/label.component';
import { IconComponent } from '../../atoms/icon.component/icon.component';

@Component({
  selector: 'app-providers-table',
  imports: [CommonModule, LabelComponent, IconComponent],
  templateUrl: './providers-table.component.html',
  styleUrl: './providers-table.component.css',
  standalone: true
})
export class ProvidersTableComponent {
  @Input() providers: Provider[] = [];
  @Output() editProvider = new EventEmitter<Provider>();
  @Output() deleteProvider = new EventEmitter<Provider>();

  onEdit(provider: Provider) {
    this.editProvider.emit(provider);
  }

  onDelete(provider: Provider) {
    this.deleteProvider.emit(provider);
  }

  getTipoLabel(tipo: string) {
    return tipo === 'reparaciones_mantenimientos'
      ? 'Mantenimiento'
      : 'Servicios';
  }
}
