import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FooterTextComponent } from '../../atoms/footer-text.component/footer-text.component';

@Component({
  selector: 'app-footer-copyright',
  imports: [CommonModule, FooterTextComponent],
  templateUrl: './footer-copyright.component.html',
  styleUrl: './footer-copyright.component.css',
  standalone: true
})
export class FooterCopyrightComponent {
  currentYear = new Date().getFullYear();
}
