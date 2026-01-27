import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./components/templates/consortium-menu.component/consortium-menu.component').then(m => m.ConsortiumMenuComponent)
  },
  {
    path: 'dashboard/:consortiumName',
    loadComponent: () => import('./components/pages/dashboard/dashboard').then(m => m.Dashboard)
  },
  {
    path: 'dashboard/:consortiumName/gastos',
    loadComponent: () => import('./components/pages/expenses/expenses').then(m => m.Expenses)
  },
  {
    path: 'dashboard/:consortiumName/gastos/carga-de-gasto',
    loadComponent: () => import('./components/pages/expense-upload/expense-upload').then(m => m.ExpenseUpload)
  }
];
