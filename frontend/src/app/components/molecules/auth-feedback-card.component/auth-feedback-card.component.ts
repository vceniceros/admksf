import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';

export type AuthFeedbackTone = 'success' | 'error' | 'neutral';

@Component({
  selector: 'app-auth-feedback-card',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './auth-feedback-card.component.html',
  styleUrl: './auth-feedback-card.component.css'
})
export class AuthFeedbackCardComponent {
  @Input() title = '';
  @Input() description = '';
  @Input() tone: AuthFeedbackTone = 'neutral';
}