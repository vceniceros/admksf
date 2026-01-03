import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-label',
  template: `<span [ngStyle]="{ color: color }" class="label">{{ text }}</span>`,
  styleUrls: ['./label.component.css']
})
export class LabelComponent {
  @Input() text!: string; 
  @Input() color: string = '#000'; 
}