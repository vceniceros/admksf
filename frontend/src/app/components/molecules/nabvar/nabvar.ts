import { Component } from '@angular/core';

@Component({
  selector: 'app-navbar',
  template: `<header class="navbar">
               <div class="navbar-left">
                 <app-icon iconHref="#building-icon" size="32" color="#2563EB"></app-icon>
                 <app-label text="ConsorcioAdmin" color="#1F2937"></app-label>
               </div>
               <app-button 
                 iconHref="#menu-icon" 
                 label=""
                 iconSize="24"
                 (onClick)="toggleMenu()">
               </app-button>
             </header>`,
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent {
  toggleMenu() {
    console.log('Menu toggled');
  }
}