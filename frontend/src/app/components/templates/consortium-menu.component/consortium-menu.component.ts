import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ConsortiumService } from '../../../services/consortium.service';
import { AuthService } from '../../../services/auth.service';
import { Consortium } from '../../../../models/consortium.model';
import { AuthUser } from '../../../../models/auth.model';
import { ConsortiumGridComponent } from '../../organism/consortium-grid.component/consortium-grid.component';
import { LabelComponent } from '../../atoms/label.component/label.component';

@Component({
  selector: 'app-consortium-menu',
  imports: [CommonModule, ConsortiumGridComponent, LabelComponent],
  templateUrl: './consortium-menu.component.html',
  styleUrl: './consortium-menu.component.css',
  standalone: true
})
export class ConsortiumMenuComponent implements OnInit {
  consortia: Consortium[] = [];
  currentUser: AuthUser | null = null;

  constructor(
    private consortiumService: ConsortiumService,
    private authService: AuthService
  ) {}

  ngOnInit() {
    this.currentUser = this.authService.user();
    this.loadConsortia();
  }

  loadConsortia() {
    this.consortiumService.getAllConsortiums().subscribe({
      next: (data: Consortium[]) => {
        this.consortia = data;
      },
      error: (error: any) => {
        console.error('Error loading consortia:', error);
      }
    });
  }
}
