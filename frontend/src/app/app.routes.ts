import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./components/templates/consortium-menu.component/consortium-menu.component').then(m => m.ConsortiumMenuComponent)
  }
];
