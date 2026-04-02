import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { LoginFormComponent } from '../../organism/login-form.component/login-form.component';

@Component({
  selector: 'app-auth-access',
  standalone: true,
  imports: [CommonModule, LoginFormComponent],
  templateUrl: './auth-access.component.html',
  styleUrl: './auth-access.component.css'
})
export class AuthAccessComponent {}