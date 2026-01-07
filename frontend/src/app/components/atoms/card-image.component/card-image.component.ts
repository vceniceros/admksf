import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-card-image',
  imports: [CommonModule],
  templateUrl: './card-image.component.html',
  styleUrl: './card-image.component.css',
  standalone: true
})
export class CardImageComponent {
  @Input() imageUrl!: string;
  @Input() alt: string = '';
}
