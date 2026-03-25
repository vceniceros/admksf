import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IconComponent } from '../../atoms/icon.component/icon.component';
import { LabelComponent } from '../../atoms/label.component/label.component';

@Component({
  selector: 'app-file-preview',
  imports: [CommonModule, IconComponent, LabelComponent],
  templateUrl: './file-preview.html',
  styleUrl: './file-preview.css',
  standalone: true
})
export class FilePreview {
  @Input() fileName!: string;
  @Output() remove = new EventEmitter<void>();

  onRemove() {
    this.remove.emit();
  }
}