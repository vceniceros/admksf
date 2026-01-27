import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-porcentage-bar',
  imports: [CommonModule],
  templateUrl: './porcentage-bar.component.html',
  styleUrl: './porcentage-bar.component.css',
  standalone: true
})
export class PorcentageBarComponent {
  @Input() percentage: number = 0;
  @Input() color: string = '#2563EB';
}
