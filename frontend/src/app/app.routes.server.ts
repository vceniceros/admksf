import { RenderMode, ServerRoute } from '@angular/ssr';

export const serverRoutes: ServerRoute[] = [
  {
    path: 'consorcios/nuevo',
    renderMode: RenderMode.Client
  },
  {
    path: 'consorcios/:consortiumId/editar',
    renderMode: RenderMode.Client
  },
  {
    path: 'dashboard/:consortiumName',
    renderMode: RenderMode.Client
  },
  {
    path: 'dashboard/:consortiumName/gastos',
    renderMode: RenderMode.Client
  },
  {
    path: 'dashboard/:consortiumName/propietarios',
    renderMode: RenderMode.Client
  },
  {
    path: 'dashboard/:consortiumName/unidades',
    renderMode: RenderMode.Client
  },
  {
    path: 'dashboard/:consortiumName/proveedores',
    renderMode: RenderMode.Client
  },
  {
    path: 'dashboard/:consortiumName/saldos-mensuales',
    renderMode: RenderMode.Client
  },
  {
    path: 'dashboard/:consortiumName/pagos',
    renderMode: RenderMode.Client
  },
  {
    path: 'dashboard/:consortiumName/pagos/carga-de-pago',
    renderMode: RenderMode.Client
  },
  {
    path: 'dashboard/:consortiumName/pagos/:idPago/editar',
    renderMode: RenderMode.Client
  },
  {
    path: 'dashboard/:consortiumName/gastos/carga-de-gasto',
    renderMode: RenderMode.Client
  },
  {
    path: 'dashboard/:consortiumName/gastos/:idGasto/editar',
    renderMode: RenderMode.Client
  },
  {
    path: '',
    renderMode: RenderMode.Client
  },
  {
    path: '**',
    renderMode: RenderMode.Client
  }
];
