import { Routes } from '@angular/router';
import { authGuard, guestGuard } from './guards/auth.guard';

export const routes: Routes = [
  {
    path: '',
    canActivate: [guestGuard],
    loadComponent: () => import('./components/templates/auth-access.component/auth-access.component').then(m => m.AuthAccessComponent)
  },
  {
    path: 'consorcios',
    canActivate: [authGuard],
    loadComponent: () => import('./components/templates/consortium-menu.component/consortium-menu.component').then(m => m.ConsortiumMenuComponent)
  },
  {
    path: 'consorcios/nuevo',
    canActivate: [authGuard],
    loadComponent: () => import('./components/pages/consortium-form/consortium-form').then(m => m.ConsortiumForm)
  },
  {
    path: 'consorcios/:consortiumId/editar',
    canActivate: [authGuard],
    loadComponent: () => import('./components/pages/consortium-form/consortium-form').then(m => m.ConsortiumForm)
  },
  {
    path: 'dashboard/:consortiumName',
    canActivate: [authGuard],
    loadComponent: () => import('./components/pages/dashboard/dashboard').then(m => m.Dashboard)
  },
  {
    path: 'dashboard/:consortiumName/gastos',
    canActivate: [authGuard],
    loadComponent: () => import('./components/pages/expenses/expenses').then(m => m.Expenses)
  },
  {
    path: 'dashboard/:consortiumName/propietarios',
    canActivate: [authGuard],
    loadComponent: () => import('./components/pages/owners/owners').then(m => m.Owners)
  },
  {
    path: 'dashboard/:consortiumName/unidades',
    canActivate: [authGuard],
    loadComponent: () => import('./components/pages/units/units').then(m => m.Units)
  },
  {
    path: 'dashboard/:consortiumName/proveedores',
    canActivate: [authGuard],
    loadComponent: () => import('./components/pages/providers/providers').then(m => m.Providers)
  },
  {
    path: 'dashboard/:consortiumName/saldos-mensuales',
    canActivate: [authGuard],
    loadComponent: () => import('./components/pages/monthly-balance/monthly-balance').then(m => m.MonthlyBalancePage)
  },
  {
    path: 'dashboard/:consortiumName/pagos',
    canActivate: [authGuard],
    loadComponent: () => import('./components/pages/payments/payments').then(m => m.Payments)
  },
  {
    path: 'dashboard/:consortiumName/pagos/carga-de-pago',
    canActivate: [authGuard],
    loadComponent: () => import('./components/pages/payment-upload/payment-upload').then(m => m.PaymentUpload)
  },
  {
    path: 'dashboard/:consortiumName/pagos/:idPago/editar',
    canActivate: [authGuard],
    loadComponent: () => import('./components/pages/payment-upload/payment-upload').then(m => m.PaymentUpload)
  },
  {
    path: 'dashboard/:consortiumName/expensas',
    canActivate: [authGuard],
    loadComponent: () => import('./components/pages/settlement/settlement').then(m => m.SettlementComponent)
  },
  {
    path: 'dashboard/:consortiumName/gastos/carga-de-gasto',
    canActivate: [authGuard],
    loadComponent: () => import('./components/pages/expense-upload/expense-upload').then(m => m.ExpenseUpload)
  },
  {
    path: 'dashboard/:consortiumName/gastos/:idGasto/editar',
    canActivate: [authGuard],
    loadComponent: () => import('./components/pages/expense-upload/expense-upload').then(m => m.ExpenseUpload)
  },
  {
    path: '**',
    redirectTo: ''
  }
];
