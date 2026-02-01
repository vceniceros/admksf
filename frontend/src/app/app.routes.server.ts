import { RenderMode, ServerRoute } from '@angular/ssr';

export const serverRoutes: ServerRoute[] = [
  {
    path: 'dashboard/:consortiumName',
    renderMode: RenderMode.Server
  },
  {
    path: 'dashboard/:consortiumName/gastos',
    renderMode: RenderMode.Server
  },
  {
    path: 'dashboard/:consortiumName/propietarios',
    renderMode: RenderMode.Server
  },
  {
    path: 'dashboard/:consortiumName/unidades',
    renderMode: RenderMode.Server
  },
  {
    path: 'dashboard/:consortiumName/proveedores',
    renderMode: RenderMode.Server
  },
  {
    path: 'dashboard/:consortiumName/saldos-mensuales',
    renderMode: RenderMode.Server
  },
  {
    path: 'dashboard/:consortiumName/pagos',
    renderMode: RenderMode.Server
  },
  {
    path: 'dashboard/:consortiumName/pagos/carga-de-pago',
    renderMode: RenderMode.Server
  },
  {
    path: 'dashboard/:consortiumName/pagos/:idPago/editar',
    renderMode: RenderMode.Server
  },
  {
    path: 'dashboard/:consortiumName/gastos/carga-de-gasto',
    renderMode: RenderMode.Server
  },
  {
    path: 'dashboard/:consortiumName/gastos/:idGasto/editar',
    renderMode: RenderMode.Server
  },
  {
    path: '',
    renderMode: RenderMode.Prerender
  },
  {
    path: '**',
    renderMode: RenderMode.Prerender
  }
];
