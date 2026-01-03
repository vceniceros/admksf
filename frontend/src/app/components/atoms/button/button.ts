import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-button',
  template: `<button class="button" [ngClass]="{ active: isActive }" (click)="onClick()">
                <app-icon [iconHref]="iconHref" [size]="iconSize" [color]="iconColor"></app-icon>
                <app-label [text]="label" [color]="labelColor"></app-label>
             </button>`,
  styleUrls: ['./button.component.css']
})
export class ButtonComponent {
  @Input() iconHref!: string; 
  @Input() label!: string; 
  @Input() isActive: boolean = false; 
  @Input() iconSize: string = '24'; 
  @Input() iconColor: string = '#000'; 
  @Input() labelColor: string = '#000'; 
  @Input() onClick!: () => void; 
}