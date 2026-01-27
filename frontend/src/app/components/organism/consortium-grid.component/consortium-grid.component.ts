import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Consortium } from '../../../../models/consortium.model';
import { ConsortiumCardComponent } from '../../molecules/consortium-card.component/consortium-card.component';

@Component({
  selector: 'app-consortium-grid',
  imports: [CommonModule, ConsortiumCardComponent],
  templateUrl: './consortium-grid.component.html',
  styleUrl: './consortium-grid.component.css',
  standalone: true
})
export class ConsortiumGridComponent {
  @Input() consortia!: Consortium[];
}
