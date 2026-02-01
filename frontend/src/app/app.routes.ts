import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./components/templates/consortium-menu.component/consortium-menu.component').then(m => m.ConsortiumMenuComponent)
  },
  {
    path: 'consorcios/nuevo',
    loadComponent: () => import('./components/pages/consortium-form/consortium-form').then(m => m.ConsortiumForm)
  },
  {
    path: 'consorcios/:consortiumId/editar',
    loadComponent: () => import('./components/pages/consortium-form/consortium-form').then(m => m.ConsortiumForm)
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
    path: 'dashboard/:consortiumName/propietarios',
    loadComponent: () => import('./components/pages/owners/owners').then(m => m.Owners)
  },
  {
    path: 'dashboard/:consortiumName/unidades',
    loadComponent: () => import('./components/pages/units/units').then(m => m.Units)
  },
  {
    path: 'dashboard/:consortiumName/proveedores',
    loadComponent: () => import('./components/pages/providers/providers').then(m => m.Providers)
  },
  {
    path: 'dashboard/:consortiumName/saldos-mensuales',
    loadComponent: () => import('./components/pages/monthly-balance/monthly-balance').then(m => m.MonthlyBalancePage)
  },
  {
    path: 'dashboard/:consortiumName/pagos',
    loadComponent: () => import('./components/pages/payments/payments').then(m => m.Payments)
  },
  {
    path: 'dashboard/:consortiumName/pagos/carga-de-pago',
    loadComponent: () => import('./components/pages/payment-upload/payment-upload').then(m => m.PaymentUpload)
  },
  {
    path: 'dashboard/:consortiumName/pagos/:idPago/editar',
    loadComponent: () => import('./components/pages/payment-upload/payment-upload').then(m => m.PaymentUpload)
  },
  {
    path: 'dashboard/:consortiumName/gastos/carga-de-gasto',
    loadComponent: () => import('./components/pages/expense-upload/expense-upload').then(m => m.ExpenseUpload)
  },
  {
    path: 'dashboard/:consortiumName/gastos/:idGasto/editar',
    loadComponent: () => import('./components/pages/expense-upload/expense-upload').then(m => m.ExpenseUpload)
  }
];
