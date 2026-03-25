import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Unit } from '../../../../models/unit.model';
import { LabelComponent } from '../../atoms/label.component/label.component';
import { IconComponent } from '../../atoms/icon.component/icon.component';

@Component({
  selector: 'app-units-table',
  imports: [CommonModule, LabelComponent, IconComponent],
  templateUrl: './units-table.component.html',
  styleUrl: './units-table.component.css',
  standalone: true
})
export class UnitsTableComponent {
  @Input() units: Unit[] = [];
  @Output() editUnit = new EventEmitter<Unit>();
  @Output() deleteUnit = new EventEmitter<Unit>();

  onEdit(unit: Unit) {
    this.editUnit.emit(unit);
  }

  onDelete(unit: Unit) {
    this.deleteUnit.emit(unit);
  }
}
