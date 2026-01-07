import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IconComponent } from '../../atoms/icon.component/icon.component';
import { FooterTextComponent } from '../../atoms/footer-text.component/footer-text.component';
import { FooterCopyrightComponent } from '../../molecules/footer-copyright.component/footer-copyright.component';

@Component({
  selector: 'app-footer',
  imports: [CommonModule, IconComponent, FooterTextComponent, FooterCopyrightComponent],
  templateUrl: './footer.component.html',
  styleUrl: './footer.component.css',
  standalone: true
})
export class FooterComponent {
}
