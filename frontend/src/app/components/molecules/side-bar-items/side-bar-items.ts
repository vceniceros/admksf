import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-sidebar-item',
  template: `<app-button [iconHref]="iconHref" [label]="label" [isActive]="isActive"></app-button>`,
  styleUrls: ['./sidebar-item.component.css']
})
export class SidebarItemComponent {
  @Input() iconHref!: string;
  @Input() label!: string;
  @Input() isActive: boolean = false;
}