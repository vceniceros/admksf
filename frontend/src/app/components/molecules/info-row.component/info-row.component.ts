import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IconComponent } from '../../atoms/icon.component/icon.component';
import { LabelComponent } from '../../atoms/label.component/label.component';

@Component({
  selector: 'app-info-row',
  imports: [CommonModule, IconComponent, LabelComponent],
  templateUrl: './info-row.component.html',
  styleUrl: './info-row.component.css',
  standalone: true
})
export class InfoRowComponent {
  @Input() iconHref!: string;
  @Input() text!: string;
  @Input() iconSize: string = '16';
  @Input() iconColor: string = '#6B7280';
  @Input() textColor: string = '#6B7280';
  @Input() fontSize: string = '14px';
}
