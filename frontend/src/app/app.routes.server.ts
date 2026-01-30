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
    path: 'dashboard/:consortiumName/gastos/carga-de-gasto',
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
