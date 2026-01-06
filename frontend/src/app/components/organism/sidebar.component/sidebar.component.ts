import { Component, Input } from '@angular/core';
import { NavbarItemComponent } from '../../molecules/navbar-item.component/navbar-item.component';


@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css'],
  standalone: true,
  imports: [NavbarItemComponent]
})
export class SidebarComponent {
  @Input() isVisible: boolean = false;
}