import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Owner } from '../../../../models/owner.model';
import { LabelComponent } from '../../atoms/label.component/label.component';
import { IconComponent } from '../../atoms/icon.component/icon.component';

@Component({
  selector: 'app-owners-table',
  imports: [CommonModule, LabelComponent, IconComponent],
  templateUrl: './owners-table.component.html',
  styleUrl: './owners-table.component.css',
  standalone: true
})
export class OwnersTableComponent {
  @Input() owners: Owner[] = [];
  @Output() editOwner = new EventEmitter<Owner>();
  @Output() deleteOwner = new EventEmitter<Owner>();

  onEdit(owner: Owner) {
    this.editOwner.emit(owner);
  }

  onDelete(owner: Owner) {
    this.deleteOwner.emit(owner);
  }
}
