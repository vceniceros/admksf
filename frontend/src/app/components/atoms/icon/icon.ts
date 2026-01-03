import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-icon',
  template: `<svg [attr.width]="size" [attr.height]="size" [attr.fill]="color">
                <use [attr.xlink:href]="iconHref"></use>
             </svg>`,
  styleUrls: ['./icon.component.css']
})
export class IconComponent {
  @Input() iconHref!: string; 
  @Input() color: string = '#000'; 
}